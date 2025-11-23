from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models.user import User
from backend.api.schemas.users.create import UserCreate

async def create_user(session: AsyncSession, user_data: UserCreate) -> None:
    """
    Регистрирует нового пользователя в системе.
    """
    user = User(**user_data.model_dump(exclude_unset=True))
    session.add(user)
    await session.commit()
