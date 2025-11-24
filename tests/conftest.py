import httpx

import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from backend.db.init_db import get_session
from backend.__main__ import app


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """
    Сессия для прямой работы с БД в тестах.
    """
    db_url = "sqlite+aiosqlite:///:memory:"
    engine = create_async_engine(db_url)

    async with engine.begin() as conn:
        from backend.db.models.base import Base
        await conn.run_sync(Base.metadata.create_all)

    async_session_factory = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    try:
        async with async_session_factory() as session:
            yield session
    finally:
        await session.close()
        await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    """
    Фикстура для тестового клиента FastAPI
    """
    async def override_get_session():
        try:
            yield db_session
        finally:
            await db_session.rollback()

    app.dependency_overrides[get_session] = override_get_session

    async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()