from datetime import timedelta

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from authx import AuthX, AuthXConfig, exceptions
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

_ph = PasswordHasher()


def _make_jwt_security() -> AuthX:
    from core.settings import get_settings

    settings = get_settings()
    config = AuthXConfig(
        JWT_SECRET_KEY=settings.JWT_SECURITY_KEY.get_secret_value(),
        JWT_TOKEN_LOCATION=["headers", "cookies"],
        JWT_REFRESH_COOKIE_NAME="refresh_token",
        JWT_COOKIE_CSRF_PROTECT=True,
        JWT_COOKIE_HTTP_ONLY=True,
        JWT_COOKIE_SECURE=settings.JWT_COOKIE_SECURE,
        JWT_COOKIE_SAMESITE=settings.JWT_COOKIE_SAMESITE,
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES),
        JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=settings.REFRESH_TOKEN_EXPIRES),
    )
    return AuthX(config=config)


jwt_security = _make_jwt_security()


def register_auth_error_handlers(app: FastAPI) -> None:
    jwt_security.handle_errors(app)

    @app.exception_handler(exceptions.JWTDecodeError)
    async def invalid_token_handler(request: Request, exc: exceptions.JWTDecodeError):
        return JSONResponse(
            status_code=401, content={"detail": "Invalid or expired token"}
        )


def hash_password(password: str) -> str:
    return _ph.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return _ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False
