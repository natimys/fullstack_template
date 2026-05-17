from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import hash_password
from modules.auth.schemas import UserRegister
from modules.users.models import User, UserRole


class UserService:
    def __init__(self, db: AsyncSession ):
        self.db = db

    async def register_user(self, user_data: UserRegister):
        query = select(User).where(User.email == user_data.email)
        result = await self.db.execute(query)
        existing_user = result.scalar_one_or_none()

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
