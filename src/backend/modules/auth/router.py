from core.security import jwt_security
from fastapi import APIRouter, Depends, HTTPException, Response
from loguru import logger

from ..users.dependencies import get_user_service
from ..users.service import UserService
from .dependencies import get_auth_service
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


@router.post("/login/")
async def login(
    data: UserLogin,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
):
    access_token, refresh_token = await auth_service.authenticate(data)

    jwt_security.set_access_cookies(access_token, response)
    jwt_security.set_refresh_cookies(refresh_token, response)

    return {"message": "success"}


@router.post("/refresh/")
async def refresh(
    response: Response,
    payload=Depends(jwt_security.refresh_token_required),
):
    user_id = payload.sub()
    access_token = jwt_security.create_access_token(uid=user_id)
    refresh_token = jwt_security.create_refresh_token(uid=user_id)

    jwt_security.set_access_token(access_token, response)
    jwt_security.set_refresh_cookies(refresh_token, response)

    return {"message": "success"}


@router.get("/me/", response_model=UserPublic)
async def me(
    payload=Depends(jwt_security.access_token_required),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_user_by_id(int(payload.sub()))


@router.get("/logout/")
async def logout(response: Response):
    response.delete_cookie(key="refresh_token")
    return {"message": "logged out"}
