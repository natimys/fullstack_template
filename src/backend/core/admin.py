"""Privileged bootstrap command; intentionally has no HTTP counterpart."""

import argparse
import asyncio
import getpass
import sys

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from core.enums import UserRole
from core.security import hash_password
from core.settings import get_settings
from modules.users.models import User


async def create_admin(email: str, name: str, password: str) -> None:
    settings = get_settings()
    engine = create_async_engine(settings.DATABASE_URL)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    try:
        async with session_maker() as session:
            existing = await session.scalar(select(User).where(User.email == email))
            if existing:
                raise SystemExit(f"A user with email {email!r} already exists.")
            session.add(
                User(
                    email=email,
                    name=name,
                    password=hash_password(password),
                    role=UserRole.ADMIN,
                    is_active=True,
                )
            )
            await session.commit()
    finally:
        await engine.dispose()


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("--email", required=True)
    create_parser.add_argument("--name", required=True)
    args = parser.parse_args()
    if sys.stdin.isatty():
        password = getpass.getpass("Password (minimum 12 characters): ")
        confirmation = getpass.getpass("Confirm password: ")
        if password != confirmation:
            raise SystemExit("Passwords do not match.")
    else:
        password = sys.stdin.readline().rstrip("\r\n")
    if len(password) < 12:
        raise SystemExit("Password must be at least 12 characters.")
    asyncio.run(create_admin(args.email, args.name, password))


if __name__ == "__main__":
    main()
