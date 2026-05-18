from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import hash_password
from modules.users.models import User, UserRole


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Возвращает пользователя по email
        :param email:
        :return: User or None
        """
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        return user

    async def get_user_by_id(self, user_id: int) -> User | None:
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        return user

    async def create_user(
            self,
            email: str,
            name: str,
            password: str,
            role: UserRole = UserRole.USER
    ) -> User:
        """
        :param email:
        :param name:
        :param password:
        :param role:
        :return:
        """
        existing_user = await self.get_user_by_email(email)

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        new_user = User(
            email=email,
            name=name,
            password=password,
            role=role
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        return new_user
