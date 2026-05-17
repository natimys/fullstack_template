from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.settings import get_settings

settings = get_settings()

engine = create_async_engine(settings.DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
