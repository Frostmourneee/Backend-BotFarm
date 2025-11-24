from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models.user import User


async def get_user_by_login(
        session: AsyncSession,
        login: str
) -> User | None:
    """
    Поиск пользователя по логину (email).

    Args:
        session: Асинхронная сессия БД
        login: Логин (email) пользователя

    Returns:
        User | None: Найденный пользователь или None
    """
    statement = select(User).where(User.login == login)
    return await session.scalar(statement)
