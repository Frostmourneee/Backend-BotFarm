from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from backend.db.models.user import User


# Борьба с состоянием гонки благодаря SELECT FOR UPDATE
async def get_user_by_id_for_update(
        session: AsyncSession,
        user_id: UUID
) -> User | None:
    """
    Получение пользователя по ID с блокировкой для обновления.

    Args:
        session: Асинхронная сессия БД
        user_id: UUID пользователя

    Returns:
        User | None: Пользователь или None если не найден
    """
    lock_statement = (
        select(User)
        .where(User.id == user_id)
        .with_for_update()
    )

    return await session.scalar(lock_statement)