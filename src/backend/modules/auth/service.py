from fastapi import Response

from core.exceptions import InvalidAuthCredentials
from core.security import verify_password,jwt_security

from modules.auth.schemas import UserLogin, UserRegister
from modules.users.models import User
from modules.users.service import UserService

class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def register(self, data: UserRegister) -> User:
        user = await self.user_service.register(
            email=data.email, name=data.name, password=data.password.get_secret_value()
        )
        return user


    async def authenticate(self, data: UserLogin) -> tuple[str, str]:
        user = await self.user_service.get_user_by_email(data.email)
        password = data.password.get_secret_value()
        if not user or not verify_password(plain_password=password, hashed_password=user.password):
            raise InvalidAuthCredentials()
        access_token = jwt_security.create_access_token(uid=str(user.id))
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!{access_token}")
        refresh_token = jwt_security.create_refresh_token(uid=str(user.id))

        return access_token, refresh_token

    # async def _get_tokens(self, user_id: str):