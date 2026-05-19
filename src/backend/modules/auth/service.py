from core.exceptions import InvalidAuthCredentials
from core.security import verify_password

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


    async def authenticate(self, data: UserLogin) -> User:
        user = await self.user_service.get_user_by_email(data.email)
        password = data.password.get_secret_value()
        if not user or not verify_password(plain_password=password, hashed_password=user.password):
            raise InvalidAuthCredentials()
        return user