from fastapi import APIRouter, Depends

from modules.users.service import UserService

from modules.users.dependencies import get_user_service
from .schemas import UserLogin, UserPublic, UserRegister
from .service import AuthService
from .module import module
router = APIRouter(prefix=module.router_prefix, tags=module.router_tags)


@router.post("/register/", response_model=UserPublic)
async def register(
    user: UserRegister, user_service: UserService = Depends(get_user_service)
):
    pass


@router.post("/login/")
async def login(user: UserLogin):
    pass


@router.get("/me/")
async def me():
    pass
