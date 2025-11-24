import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from backend.db.models.user import User
from backend.api.schemas.users.create import UserCreate
from backend.crud.users.create import create_user
import uuid


@pytest.mark.asyncio
async def test_create_user_success(
        db_session: AsyncSession,
        user_create_data
):
    """
    Тест успешного создания пользователя
    """
    user_data = UserCreate(**user_create_data)
    await create_user(db_session, user_data)

    result = await db_session.execute(
        select(User).where(User.login == user_create_data["login"])
    )
    user = result.scalar_one()

    assert user.login == user_create_data["login"]
    assert user.project_id == user_create_data["project_id"]
    assert user.env == user_create_data["env"]
    assert user.domain == user_create_data["domain"]
    assert user.locktime is None


@pytest.mark.asyncio
async def test_create_user_password_is_hashed(
        db_session: AsyncSession,
        user_create_data
):
    """
    Тест, что пароль правильно хэшируется
    """
    user_data = UserCreate(**user_create_data)
    await create_user(db_session, user_data)

    result = await db_session.execute(
        select(User).where(User.login == user_create_data["login"])
    )
    user = result.scalar_one()

    assert user.password != user_create_data["password"]
    assert len(user.password) > 20


@pytest.mark.asyncio
async def test_create_user_with_same_login_fails(
        db_session: AsyncSession,
        user_create_data
):
    """
    Тест, что нельзя создать двух пользователей с одинаковым логином
    """
    user_data = UserCreate(**user_create_data)
    await create_user(db_session, user_data)

    user_data_duplicate = UserCreate(
        login=user_create_data["login"],
        password="123",
        project_id=uuid.uuid4(),
        env="prod",
        domain="regular"
    )

    with pytest.raises(IntegrityError):
        await create_user(db_session, user_data_duplicate)
        await db_session.commit()

    await db_session.rollback()

    result = await db_session.execute(
        select(User).where(User.login == user_create_data["login"])
    )
    users = result.scalars().all()

    assert len(users) == 1
