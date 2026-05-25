from core.security import jwt_security
from fastapi import APIRouter, Depends, HTTPException, Response
from loguru import logger

from ..users.dependencies import get_user_service
from ..users.service import UserService
from .dependencies import get_auth_service, login_and_set_cookies, refresh_session_and_set_cookies
from .module import module
from .schemas import UserLogin, UserPublic, UserRegister
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
    payload=Depends(jwt_security.access_token_required),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_user_by_id(int(payload.sub))


@router.post("/refresh/")
async def refresh(
    status: dict = Depends(refresh_session_and_set_cookies)
):
    return status


@router.post("/login/")
async def login(
    result: dict = Depends(login_and_set_cookies)
):
    return result


@router.get("/logout/")
async def logout(response: Response):
    response.delete_cookie(key="refresh_token")
    response.delete_cookie(key="access_token")
    return {"message": "logged out"}
