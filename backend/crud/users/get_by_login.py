from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.db.models.user import User


async def get_user_by_login(
        session: AsyncSession,
        login: str
) -> User | None:
    """
    Ищет пользователя по логину (email)
    """
    statement = select(User).where(User.login == login)
    return await session.scalar(statement)
