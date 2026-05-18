from fastapi import HTTPException

from core.security import verify_password
from modules.auth.schemas import UserRegister, UserLogin
from modules.users.service import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def register(self, data: UserRegister):
        return await self.user_service.create_user(
            email=data.email,
            name=data.name,
            password=data.password.get_secret_value()
        )

    async def authenticate(self, data: UserLogin):
        user = await self.user_service.get_user_by_email(data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        if not verify_password(data.password.get_secret_value()):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        return user
