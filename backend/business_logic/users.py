from pydantic import AwareDatetime
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from backend.business_logic.exceptions import UserNotFound, UserNotBot
from backend.crud.users.get_by_id_for_update import get_by_id_for_update

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
    user = await get_by_id_for_update(session, user_id)

    if not user:
        raise UserNotFound()

    if user.domain != 'canary':
        raise UserNotBot()

    should_unlock_unlocked = user.locktime is None and locktime is None
    should_lock_locked = user.locktime is not None and locktime is not None
    is_same_state = should_lock_locked or should_unlock_unlocked
    if is_same_state:
        return True


    user.locktime = locktime
    await session.commit()

    return False