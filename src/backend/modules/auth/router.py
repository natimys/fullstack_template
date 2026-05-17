from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import hash_password, verify_password
from database.dependencies import get_db
from modules.users.service import UserService
from .schemas import UserPublic, UserRegister, UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])


def get_user_service(db: AsyncSession = Depends(get_db)):
    return UserService(db)


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
