from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import hash_password
from database.dependencies import get_db
from modules.users.service import UserService
from .schemas import UserPublic, UserRegister

router = APIRouter(prefix="/auth", tags=["auth"])


def get_user_service(db: AsyncSession = Depends(get_db)):
    return UserService(db)


@router.post("/register/", response_model=UserPublic)
async def register(
        user: UserRegister, user_service: UserService = Depends(get_user_service)
):
    print(hash_password(user.password.get_secret_value()))
    new_user = await user_service.register_user(user)

    return new_user


@router.post("/login/")
async def login():
    pass


@router.post("/logout/")
async def logout():
    pass


@router.get("/whoami/")
async def whoami():
    pass
