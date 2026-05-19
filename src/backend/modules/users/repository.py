from core.exceptions import UserAlreadyExists
from sqlalchemy import select

from .models import User, UserRole


class UserRepository:
    def __init__(self, db):
        self.db = db

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Возвращает пользователя по emai
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
        self, email: str, name: str, password: str, role: UserRole
    ) -> User | None:
        new_user = User(email=email, name=name, password=password, role=role)
        self.db.add(new_user)
        await self.db.commit()
        return new_user

    async def save_user(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
