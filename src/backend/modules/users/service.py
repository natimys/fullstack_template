from core.exceptions import UserAlreadyExists
from core.security import hash_password

from .models import User
from core.enums import UserRole
from .repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.repository.get_user_by_id(user_id)

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.repository.get_user_by_email(email)

    async def list_users(self, page: int = 1, size: int = 10) -> tuple[list[User], int]:
        skip = (page - 1) * size
        users = await self.repository.get_users(skip=skip, limit=size)
        total = await self.repository.count_users()
        return users, total

    async def register(self, email: str, name: str, password: str) -> User:
        user_exists = await self.repository.get_user_by_email(email)
        if user_exists:
            raise UserAlreadyExists()
        user = await self.repository.create_user(
            email, name, hash_password(password), role=UserRole.USER
        )
        return user

    async def create_user(self, email: str, name: str, password: str, role: UserRole = UserRole.USER) -> User:
        user_exists = await self.repository.get_user_by_email(email)
        if user_exists:
            raise UserAlreadyExists()
        return await self.repository.create_user(
            email, name, hash_password(password), role=role
        )

    async def update_user(self, user_id: int, **kwargs) -> User | None:
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            return None
        if "password" in kwargs and kwargs["password"]:
            kwargs["password"] = hash_password(kwargs["password"])
        for key, value in kwargs.items():
            if value is not None and hasattr(user, key):
                setattr(user, key, value)
        return await self.repository.update_user(user)

    async def delete_user(self, user_id: int) -> bool:
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            return False
        await self.repository.delete_user(user)
        return True