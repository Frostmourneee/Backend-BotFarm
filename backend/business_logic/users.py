from pydantic import AwareDatetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from uuid import UUID

from backend.business_logic.exceptions import UserNotFound
from backend.db.models.user import User

async def update_user_lock(
        session: AsyncSession,
        user_id: UUID,
        locktime: AwareDatetime | None
) -> bool:
    # Борьба с состоянием гонки благодаря SELECT FOR UPDATE
    lock_statement = (
        select(User)
        .where(User.id == user_id)
        .with_for_update()
    )
    user = await session.scalar(lock_statement)

    if not user:
        raise UserNotFound()

    # Идемпотентное поведение, если был
    # заблокирован, то ничего не происходит
    if user.locktime is None:
        return False

    update_stmt = (
        update(User)
        .where(User.id == user_id)
        .values(locktime=locktime)
    )
    await session.execute(update_stmt)

    return True
