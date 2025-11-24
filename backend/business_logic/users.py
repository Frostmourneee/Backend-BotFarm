from uuid import UUID

from pydantic import AwareDatetime
from sqlalchemy.ext.asyncio import AsyncSession

from backend.business_logic.exceptions import UserNotBot, UserNotFound
from backend.crud.users.get_by_id_for_update import get_user_by_id_for_update


async def update_user_lock(
        session: AsyncSession,
        user_id: UUID,
        locktime: AwareDatetime | None
) -> bool:
    """
    Установка или снятие блокировки пользователя-бота.

    Args:
        session: Асинхронная сессия БД
        user_id: UUID пользователя
        locktime: Время блокировки (None - разблокировать)

    Returns:
        bool: True если состояние не изменилось, False если выполнено изменение

    Raises:
        UserNotFound: Пользователь не найден
        UserNotBot: Пользователь не является ботом (canary домен)
    """
    user = await get_user_by_id_for_update(session, user_id)

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
