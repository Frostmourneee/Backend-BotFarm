import httpx

import pytest_asyncio
from faker import Faker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
import uuid

from backend.db.init_db import get_session
from backend.__main__ import app

fake = Faker()

def sqlite_gen_random_uuid():
    return str(uuid.uuid4())

def sqlite_now():
    from datetime import datetime, UTC
    return datetime.now(tz=UTC).replace(tzinfo=None)

@pytest_asyncio.fixture(scope="function")
async def db_session():
    """
    Сессия для прямой работы с БД в тестах.
    """
    db_url = "sqlite+aiosqlite:///:memory:"
    engine = create_async_engine(db_url)

    @event.listens_for(engine.sync_engine, "connect")
    def connect(dbapi_connection, connection_record):
        dbapi_connection.create_function(
            "gen_random_uuid",
            0,
            sqlite_gen_random_uuid
        )
        dbapi_connection.create_function("now", 0, sqlite_now)

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

@pytest_asyncio.fixture
async def user_create_data():
    """
    Фикстура с данными для создания пользователя
    """
    return {
        "login": fake.email(),
        "password": "password",
        "project_id": uuid.uuid4(),
        "env": fake.random_element(["prod", "stage", "preprod"]),
        "domain": fake.random_element(["regular", "canary"])
    }

@pytest_asyncio.fixture
async def regular_user_create_data():
    """
    Фикстура с данными для создания regular пользователя
    """
    return {
        "login": fake.email(),
        "password": "password",
        "project_id": uuid.uuid4(),
        "env": fake.random_element(["prod", "stage", "preprod"]),
        "domain": "regular"
    }


@pytest_asyncio.fixture
async def auth_headers(client, regular_user_create_data):
    """
    Фикстура для получения авторизационных headers
    """
    user_data_for_api = {
        **regular_user_create_data,
        "project_id": str(regular_user_create_data["project_id"])
    }

    await client.post("/api/v1/users", json=user_data_for_api)

    login_response = await client.post(
        "/api/v1/login",
        data={
            "username": regular_user_create_data["login"],
            "password": regular_user_create_data["password"]
        }
    )
    token = login_response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}