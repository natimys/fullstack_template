from database.dependencies import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from modules.users.service import UserService


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)
