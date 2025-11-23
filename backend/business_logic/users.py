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
    """
    Устанавливает или снимает блокировку пользователя

    locktime=None - снять блокировку
    locktime=datetime - установить блокировку

    Возвращает True, если блокировали блокированного
    или разблокировали разблокированного. Т.е. возврат -- индикатор
    того, можно ли не делать никакого update
    """
    # Борьба с состоянием гонки благодаря SELECT FOR UPDATE
    lock_statement = (
        select(User)
        .where(User.id == user_id)
        .with_for_update()
    )
    user = await session.scalar(lock_statement)

    if not user:
        raise UserNotFound()


    should_unlock_unlocked = user.locktime is None and locktime is None
    should_lock_locked = user.locktime is not None and locktime is not None
    is_same_state = should_lock_locked or should_unlock_unlocked
    if is_same_state:
        return True


    update_stmt = (
        update(User)
        .where(User.id == user_id)
        .values(locktime=locktime)
    )
    await session.execute(update_stmt)
    await session.commit()

    return False