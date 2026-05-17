from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    DATABASE_URL: str
    ALEMBIC_DATABASE_URL: str
    REDIS_URL: str
    SECURITY_KEY: SecretStr

    REFRESH_TOKEN_EXPIRES: int  # в днях
    ACCESS_TOKEN_EXPIRES: int  # в минутах

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra='ignore'
    )


@lru_cache
def get_settings():
    return Settings()
