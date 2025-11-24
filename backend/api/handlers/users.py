from datetime import UTC, datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.schemas.users.create import UserCreate, UserCreateResponse
from backend.api.schemas.users.get_all import (GET_ALL_RESPONSES,
                                               UserGetAllResponse)
from backend.api.schemas.users.lock import LOCK_RESPONSES, UserLockResponse
from backend.api.schemas.users.unlock import UserUnlockResponse
from backend.business_logic.exceptions import UserNotBot, UserNotFound
from backend.business_logic.users import update_user_lock
from backend.crud.users.create import create_user as crud_create_user
from backend.crud.users.get_all import get_all_users
from backend.db.init_db import get_session
from backend.db.models.user import User
from backend.utils.auth import require_regular_user

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
    """
    Создание нового пользователя.

    Args:
        user_data: Данные для создания пользователя
        session: Сессия БД

    Returns:
        UserCreateResponse: Пустой ответ об успешном создании

    Raises:
        HTTPException: 409 - если пользователь с таким логином уже существует
    """
    try:
        await crud_create_user(session, user_data)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже есть в БД"
        )

    return UserCreateResponse()


@api_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[UserGetAllResponse],
    responses=GET_ALL_RESPONSES,
)
async def get_users(
        session: AsyncSession = Depends(get_session),
        user: User = Depends(require_regular_user)
) -> list[UserGetAllResponse]:
    """
    Получение списка всех пользователей.

    Args:
        session: Сессия БД
        user: Авторизованный regular пользователь

    Returns:
        list[UserGetAllResponse]: Список пользователей
    """
    users = await get_all_users(session)
    return users


@api_router.post(
    "/{user_id}/lock",
    status_code=status.HTTP_200_OK,
    response_model=UserLockResponse,
    responses=LOCK_RESPONSES
)
async def acquire_lock(
        user_id: UUID,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(require_regular_user)
) -> UserLockResponse:
    """
    Блокировка пользователя-бота.

    Args:
        user_id: UUID пользователя для блокировки
        session: Сессия БД
        user: Авторизованный regular пользователь

    Returns:
        UserLockResponse: Результат операции блокировки

    Raises:
        HTTPException: 404 - пользователь не найден
        HTTPException: 422 - пользователь не является ботом
    """
    try:
        locktime = datetime.now(tz=UTC)
        is_same_state = await update_user_lock(session, user_id, locktime)
        if is_same_state:
            return UserLockResponse(message="Пользователь уже заблокирован")

        return UserLockResponse()
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    except UserNotBot:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Данный пользователь не бот, не годится для теста"
        )


@api_router.delete(
    "/{user_id}/lock",
    status_code=status.HTTP_200_OK,
    response_model=UserUnlockResponse,
    responses=LOCK_RESPONSES
)
async def release_lock(
        user_id: UUID,
        session: AsyncSession = Depends(get_session),
        user: User = Depends(require_regular_user)
) -> UserUnlockResponse:
    """
    Разблокировка пользователя-бота.

    Args:
        user_id: UUID пользователя для разблокировки
        session: Сессия БД
        user: Авторизованный regular пользователь

    Returns:
        UserUnlockResponse: Результат операции разблокировки

    Raises:
        HTTPException: 404 - пользователь не найден
        HTTPException: 422 - пользователь не является ботом
    """
    try:
        is_same_state = await update_user_lock(session, user_id, None)
        if is_same_state:
            return UserUnlockResponse(message="Пользователь не был блокирован")

        return UserUnlockResponse()
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    except UserNotBot:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Данный пользователь не бот, не годится для теста"
        )