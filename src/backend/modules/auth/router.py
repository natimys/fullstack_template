from fastapi import APIRouter, Depends, Response
from core.dependencies import get_current_user
from core.security import jwt_security

from .dependencies import (
    get_auth_service,
    login_and_set_cookies,
    logout_session,
    refresh_session_and_set_cookies,
)
from .module import module
from .schemas import UserPublic, UserRegister
from .service import AuthService

router = APIRouter(prefix=module.router_prefix, tags=module.router_tags)


@router.post("/register/", response_model=UserPublic)
async def register(
    data: UserRegister, auth_service: AuthService = Depends(get_auth_service)
):
    user = await auth_service.register(data)
    return user


@router.get("/me/", response_model=UserPublic)
async def me(
    user=Depends(get_current_user),
):
    return user


@router.post("/refresh/")
async def refresh(status: dict = Depends(refresh_session_and_set_cookies)):
    return status


@router.post("/login/")
async def login(result: dict = Depends(login_and_set_cookies)):
    return result


@router.post("/logout/")
async def logout(response: Response, _=Depends(logout_session)):
    jwt_security.unset_refresh_cookies(response)
    jwt_security.unset_access_cookies(response)
    return {"message": "logged out"}
