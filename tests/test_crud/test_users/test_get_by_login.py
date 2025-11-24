import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.schemas.users.create import UserCreate
from backend.crud.users.create import create_user
from backend.crud.users.get_by_login import get_user_by_login


@pytest.mark.asyncio
async def test_get_user_by_login_success(
        db_session: AsyncSession,
        user_create_data
):
    """
    Тест успешного поиска пользователя по логину
    """
    user_data = UserCreate(**user_create_data)
    await create_user(db_session, user_data)

    user = await get_user_by_login(db_session, user_create_data["login"])

    assert user is not None
    assert user.login == user_create_data["login"]
    assert user.project_id == user_create_data["project_id"]


@pytest.mark.asyncio
async def test_get_user_by_login_not_found(db_session: AsyncSession):
    """
    Тест поиска несуществующего пользователя по логину
    """
    user = await get_user_by_login(db_session, "123@abc.com")

    assert user is None