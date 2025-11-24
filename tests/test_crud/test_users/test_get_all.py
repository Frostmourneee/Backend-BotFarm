import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.schemas.users.create import UserCreate
from backend.crud.users.create import create_user
from backend.crud.users.get_all import get_all_users
from backend.db.models.user import User
from tests.conftest import fake


@pytest.mark.asyncio
async def test_get_all_users_empty_db(db_session: AsyncSession):
    """
    Тест получения всех пользователей из пустой БД
    """
    users = await get_all_users(db_session)

    assert users == []
    assert len(users) == 0


@pytest.mark.asyncio
async def test_get_all_users_with_data(
        db_session: AsyncSession,
        user_create_data
):
    """
    Тест получения всех пользователей когда в БД есть данные
    """
    user_data = UserCreate(**user_create_data)
    await create_user(db_session, user_data)

    users = await get_all_users(db_session)

    assert len(users) == 1
    assert users[0].login == user_create_data["login"]
    assert users[0].project_id == user_create_data["project_id"]


@pytest.mark.asyncio
async def test_get_all_users_multiple_users(db_session: AsyncSession):
    """
    Тест получения нескольких пользователей
    """
    for i in range(3):
        user_data = UserCreate(
            login=fake.email(),
            password="password",
            project_id=uuid.uuid4(),
            env=fake.random_element(["prod", "stage", "preprod"]),
            domain=fake.random_element(["regular", "canary"])
        )
        await create_user(db_session, user_data)

    users = await get_all_users(db_session)

    assert len(users) == 3
    assert all(isinstance(user, User) for user in users)
