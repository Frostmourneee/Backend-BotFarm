import asyncio

from sqlalchemy.exc import IntegrityError

from backend.api.schemas.users.create import UserCreate
from backend.crud.users.create import create_user
from backend.db.init_db import async_session_factory


async def create_admin_user():
    async with async_session_factory() as session:
        user_data = UserCreate(
            login='admin@admin.com',
            password='admin',
            project_id='2406ec3f-d504-4001-b2e3-5a846d0c3b31',
            env='prod',
            domain='regular'
        )

        try:
            await create_user(session, user_data)
        except IntegrityError:
            pass


if __name__ == "__main__":
    asyncio.run(create_admin_user())

