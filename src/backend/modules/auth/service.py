from modules.auth.schemas import UserRegister
from modules.users.service import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def register(self, data: UserRegister):
        existing_user = await self.user_service.get_user_by_email(data.email)
