from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.schemas.users.create import UserCreate
from backend.db.models.user import User
from backend.utils.security import get_password_hash


async def create_user(
        session: AsyncSession,
        user_data: UserCreate
) -> None:
    """
    Создание нового пользователя в БД.

    Args:
        session: Асинхронная сессия БД
        user_data: Данные для создания пользователя
    """
    hashed_password = get_password_hash(user_data.password)
    user = User(
        **user_data.model_dump(exclude_unset=True, exclude={"password"}),
        password=hashed_password
    )

    session.add(user)
    await session.commit()