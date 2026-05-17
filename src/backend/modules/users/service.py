from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import hash_password
from modules.auth.schemas import UserRegister
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

    async def add_user(self, user_data: UserRegister) -> User:
        """
        Создает пользователя в базе данных
        :param user_data: поля с UserRegister
        :return: User
        """
        existing_user = await self.get_user_by_email(user_data.email)

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = hash_password(user_data.password.get_secret_value())

        new_user = User(
            email=user_data.email,
            name=user_data.name,
            password=hashed_password,
            role=UserRole.USER
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        return new_user
