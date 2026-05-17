from datetime import timedelta

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from authx import AuthX, AuthXConfig

from core.settings import get_settings

settings = get_settings()

ph = PasswordHasher()

config = AuthXConfig(
    JWT_SECRET_KEY=settings.SECURITY_KEY.get_secret_value(),

    JWT_TOKEN_LOCATION=["headers", "cookies"],

    JWT_COOKIE_SECURE=True,
    JWT_COOKIE_CSRF_PROTECT=True,
    JWT_COOKIE_SAMESITE="strict",

    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES),
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=settings.REFRESH_TOKEN_EXPIRES),
)

authx = AuthX(config=config)


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, ph.hash(hashed_password))
    except VerifyMismatchError:
        return False
