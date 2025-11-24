from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from backend.config.utils import get_settings


def create_session_factory():
    settings = get_settings()
    engine = create_async_engine(settings.database_uri)
    return sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async_session_factory = create_session_factory()


async def get_session():
    async with async_session_factory() as session:
        yield session
