from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from uuid import UUID

from backend.api.schemas.users.create import UserCreate, UserCreateResponse
from backend.api.schemas.users.get_all import UserGetAllResponse
from backend.api.schemas.users.lock import UserLockResponse
from backend.api.schemas.users.unlock import UserUnlockResponse
from backend.db.init_db import get_session
from backend.crud.users.create import create_user as crud_create_user
from backend.crud.users.get_all import get_all_users
from backend.business_logic.users import release_lock as release_user_lock
from backend.business_logic.exceptions import UserNotFound

api_router = APIRouter(prefix="/users", tags=["users"])

@api_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserCreateResponse,
    responses={
        status.HTTP_409_CONFLICT: {
            "content": {
                "application/json": {
                    "example": {"detail": "Пользователь уже есть в БД"}
                }
            }
        }
    }
)
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
) -> UserCreateResponse:
    try:
        await crud_create_user(session, user_data)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже есть в БД"
        )

    return UserCreateResponse()

@api_router.get("", response_model=list[UserGetAllResponse])
async def get_users(
    session: AsyncSession = Depends(get_session)
) -> list[UserGetAllResponse]:
    users = await get_all_users(session)
    return users

@api_router.post("/{user_id}/lock", response_model=UserLockResponse)
async def acquire_lock(
    user_id: UUID,
    session: AsyncSession = Depends(get_session)
) -> UserLockResponse:
    pass

@api_router.delete(
    "/{user_id}/lock",
    status_code=status.HTTP_200_OK,
    response_model=UserUnlockResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {
                    "example": {"detail": "Пользователь не найден"}
                }
            }
        }
    }
)
async def release_lock(
    user_id: UUID,
    session: AsyncSession = Depends(get_session)
) -> UserUnlockResponse:
    try:
        was_locked = await release_user_lock(session, user_id)
        if was_locked:
            return UserUnlockResponse()

        return UserUnlockResponse("Пользователь не был блокирован")
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
