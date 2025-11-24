import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.crud.users.get_by_id_for_update import get_user_by_id_for_update
import uuid

@pytest.mark.asyncio
async def test_get_user_by_id_for_update_not_found(db_session: AsyncSession):
    """
    Тест получения несуществующего пользователя по id для апдейта
    """
    non_existent_id = uuid.uuid4()
    user = await get_user_by_id_for_update(db_session, non_existent_id)

    assert user is None