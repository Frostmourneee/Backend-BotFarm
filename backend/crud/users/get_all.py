from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models.user import User


async def get_all_users(session: AsyncSession) -> list[User]:
    """
    Получение списка всех пользователей ботфермы.

    Args:
        session: Асинхронная сессия БД

    Returns:
        list[User]: Список всех пользователей с их данными
    """
    all_users = await session.execute(select(User))
    return all_users.scalars().all()

    # Я думаю, что из формулировки задания я должен вернуть пользователя
    # вместе с паролем. Хотя обычно это очень опасная ситуация и так делать
    # нельзя, здесь у нас не пользователи, а боты, нам как раз нужно
    # возвращать их креды
