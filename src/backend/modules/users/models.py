from enum import Enum

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    role: Mapped[UserRole] = mapped_column()
    email: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String(50))

    password: Mapped[str] = mapped_column(String)
