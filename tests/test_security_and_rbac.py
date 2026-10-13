import asyncio
from datetime import datetime, timedelta
from http.cookies import SimpleCookie
from types import SimpleNamespace

import pytest
from authx import TokenPayload
from fastapi import Depends, FastAPI, HTTPException
from httpx import ASGITransport, AsyncClient
from starlette.responses import Response

from core.dependencies import get_current_user, require_permission
from core.enums import (
    ROLE_PARENTS,
    Permission,
    UserRole,
    _role_permissions,
    has_permission,
)
from core.security import jwt_security, register_auth_error_handlers
from modules.auth.schemas import UserRegister
from modules.auth.service import AuthService
from modules.users.models import User
from modules.users.schemas import UserUpdate
from modules.users.service import UserService


def make_user(role: UserRole = UserRole.USER, *, active: bool = True) -> User:
    return User(
        id=8,
        email="person@example.com",
        name="Person",
        password="hashed",
        role=role,
        is_active=active,
        session_version=3,
        created_at=datetime.now(),
    )


def test_admin_inherits_user_permissions_and_role_cycles_fail(monkeypatch):
    assert has_permission(UserRole.ADMIN, Permission.AUTH_READ)
    assert has_permission(UserRole.ADMIN, Permission.USERS_READ)
    assert not has_permission(UserRole.USER, Permission.USERS_READ)

    monkeypatch.setitem(ROLE_PARENTS, UserRole.USER, (UserRole.ADMIN,))
    with pytest.raises(ValueError, match="cycle"):
        _role_permissions(UserRole.USER, set())


def test_users_permission_dependency_denies_regular_user():
    check = require_permission(Permission.USERS_READ)
    with pytest.raises(HTTPException) as error:
        asyncio.run(check(user=make_user()))
    assert error.value.status_code == 403
    assert asyncio.run(check(user=make_user(UserRole.ADMIN))).role == UserRole.ADMIN


class UserLookup:
    def __init__(self, user):
        self.user = user

    async def get_user_by_id(self, user_id: int):
        return self.user if user_id == 8 else None


@pytest.mark.parametrize(
    ("user", "version", "accepted"),
    [
        (make_user(), 3, True),
        (make_user(), 2, False),
        (make_user(active=False), 3, False),
        (None, 3, False),
    ],
)
def test_current_user_is_loaded_and_session_version_checked(user, version, accepted):
    payload = TokenPayload(sub="8", type="access", session_version=version)
    if accepted:
        resolved = asyncio.run(
            get_current_user(payload=payload, user_service=UserLookup(user))
        )
        assert resolved is user
    else:
        with pytest.raises(HTTPException) as error:
            asyncio.run(
                get_current_user(payload=payload, user_service=UserLookup(user))
            )
        assert error.value.status_code == 401


class RegistrationRepository:
    def __init__(self):
        self.created_role = None

    async def get_user_by_email(self, email):
        return None

    async def create_user(self, email, name, password, role):
        self.created_role = role
        return SimpleNamespace(email=email, role=role)


def test_registration_never_accepts_a_public_role():
    data = UserRegister.model_validate(
        {
            "email": "person@example.com",
            "name": "Person",
            "password": "secret",
            "role": "admin",
        }
    )
    repository = RegistrationRepository()
    created = asyncio.run(
        UserService(repository).register(
            data.email, data.name, data.password.get_secret_value()
        )
    )
    assert created.role is UserRole.USER
    assert repository.created_role is UserRole.USER


def test_tokens_keep_session_version_and_token_type_separate():
    service = AuthService(user_service=object())
    access, refresh = service.generate_tokens(8, 3, UserRole.USER)
    key = jwt_security.config.JWT_SECRET_KEY
    access_payload = TokenPayload.decode(access, key)
    refresh_payload = TokenPayload.decode(refresh, key)
    assert access_payload.type == "access"
    assert refresh_payload.type == "refresh"
    assert getattr(access_payload, "session_version") == 3
    assert getattr(refresh_payload, "session_version") == 3


def test_cookie_csrf_is_enabled():
    assert jwt_security.config.JWT_COOKIE_CSRF_PROTECT is True


def test_unauthenticated_users_api_is_rejected_and_regular_role_gets_403():
    app = FastAPI()
    register_auth_error_handlers(app)

    @app.get("/users")
    async def users(user=Depends(require_permission(Permission.USERS_READ))):
        return {"user_id": user.id}

    async def exercise():
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            assert (await client.get("/users")).status_code == 401
            app.dependency_overrides[get_current_user] = lambda: make_user()
            assert (await client.get("/users")).status_code == 403
            app.dependency_overrides[get_current_user] = lambda: make_user(
                UserRole.ADMIN
            )
            response = await client.get("/users")
            assert response.status_code == 200
            assert response.json() == {"user_id": 8}

    asyncio.run(exercise())


def test_cookie_auth_requires_csrf_header_and_sets_http_only_cookie():
    app = FastAPI()
    register_auth_error_handlers(app)

    @app.post("/unsafe")
    async def unsafe(payload=Depends(jwt_security.access_token_required)):
        return {"user_id": payload.sub}

    token = jwt_security.create_access_token(uid="8")
    cookie_response = Response()
    jwt_security.set_access_cookies(token, cookie_response)
    cookies = SimpleCookie()
    for value in cookie_response.headers.getlist("set-cookie"):
        cookies.load(value)
    cookie_values = {name: morsel.value for name, morsel in cookies.items()}
    access_cookie = cookies["access_token_cookie"]
    assert access_cookie["httponly"]
    assert access_cookie["samesite"] == "lax"

    async def exercise():
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
            cookies=cookie_values,
        ) as client:
            denied = await client.post("/unsafe")
            assert denied.status_code == 401
            accepted = await client.post(
                "/unsafe",
                headers={"X-CSRF-TOKEN": cookies["csrf_access_token"].value},
            )
            assert accepted.status_code == 200

    asyncio.run(exercise())


def test_expired_and_wrong_type_access_tokens_are_rejected():
    app = FastAPI()
    register_auth_error_handlers(app)

    @app.get("/protected")
    async def protected(payload=Depends(jwt_security.access_token_required)):
        return {"user_id": payload.sub}

    expired = jwt_security.create_access_token(uid="8", expiry=timedelta(seconds=-1))
    refresh = jwt_security.create_refresh_token(uid="8")

    async def exercise():
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            expired_response = await client.get(
                "/protected", headers={"Authorization": f"Bearer {expired}"}
            )
            wrong_type_response = await client.get(
                "/protected", headers={"Authorization": f"Bearer {refresh}"}
            )
            assert expired_response.status_code == 401
            assert wrong_type_response.status_code == 401

    asyncio.run(exercise())


def test_deactivation_and_password_change_revoke_existing_session_versions():
    user = make_user()

    class UpdateRepository:
        async def get_user_by_id(self, user_id):
            return user

        async def update_user(self, updated):
            return updated

    service = UserService(UpdateRepository())
    asyncio.run(service.update_user(user.id, UserUpdate(is_active=False)))
    assert user.session_version == 4
    assert user.is_active is False
    asyncio.run(
        service.update_user(user.id, UserUpdate(password="a-new-password-value"))
    )
    assert user.session_version == 5


def test_role_change_revokes_existing_access_token():
    user = make_user(UserRole.ADMIN)

    class UpdateRepository:
        async def get_user_by_id(self, user_id):
            return user

        async def update_user(self, updated):
            return updated

    asyncio.run(
        UserService(UpdateRepository()).update_user(
            user.id, UserUpdate(role=UserRole.USER)
        )
    )
    assert user.role is UserRole.USER
    assert user.session_version == 4

    stale_payload = TokenPayload(sub="8", type="access", session_version=3)
    with pytest.raises(HTTPException) as error:
        asyncio.run(
            get_current_user(payload=stale_payload, user_service=UserLookup(user))
        )
    assert error.value.status_code == 401
    assert not has_permission(user.role, Permission.USERS_READ)
