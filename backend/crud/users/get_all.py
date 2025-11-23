from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.db.models.user import User

async def get_all_users(session: AsyncSession) -> list[User]:
    """
    Возвращает всех пользователей с ботофермы
    """
    result = await session.execute(select(User))
    return result.scalars().all()

    # Я думаю, что из формулировки задания я должен вернуть пользователя
    # вместе с паролем. Хотя обычно это очень опасная ситуация и так делать
    # нельзя, здесь у нас не пользователи, а боты, нам как раз нужно
    # возвращать их креды