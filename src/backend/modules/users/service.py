from core.exceptions import UserAlreadyExists
from core.security import hash_password
from .models import UserRole
from .repository import UserRepository

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_user_by_id(self, user_id: int):
        return await self.repository.get_user_by_id(user_id)

    async def get_user_by_email(self, email: str):
        return await self.repository.get_user_by_email(email)

    async def register(self, email: str, name: str, password: str):
        user_exists = await self.repository.get_user_by_email(email)
        if user_exists:
            raise UserAlreadyExists()
        user = await self.repository.create_user(
            email,
            name,
            hash_password(password),
            role=UserRole.USER
        )
        return user

    async def change_password(self, email: str, new_password: str):
        user = await self.repository.get_user_by_email(email)
        if not user:
            return
        user.password = hash_password(new_password)
        await self.repository.save_user(user)