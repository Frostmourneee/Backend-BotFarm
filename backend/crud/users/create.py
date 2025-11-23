from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models.user import User
from backend.api.schemas.users.create import UserCreate
from backend.db.utils import get_password_hash

async def create_user(
        session: AsyncSession,
        user_data: UserCreate
) -> None:
    """
    Регистрирует нового пользователя в системе
    """
    hashed_password = get_password_hash(user_data.password)
    user = User(
        **user_data.model_dump(exclude_unset=True, exclude={"password"}),
        password=hashed_password
    )

    session.add(user)