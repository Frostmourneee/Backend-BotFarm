from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.schemas.auth.login import LoginResponse
from backend.business_logic.exceptions import UserNotFound, UserNotRegular
from backend.config.utils import get_settings
from backend.db.init_db import get_session
from backend.utils.auth import authenticate_user, create_access_token

api_router = APIRouter(tags=["Authentification"])


@api_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "content": {
                "application/json": {
                    "example": {"detail": "Неверный логин или пароль"}
                }
            }
        },
        status.HTTP_403_FORBIDDEN: {
            "content": {
                "application/json": {
                    "example": {"detail": "Доступ только для regular"}
                }
            }
        }
    }
)
async def login(
        login_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_session),
) -> LoginResponse:
    """
    Аутентификация пользователя и выдача JWT токена доступа.

    Процесс аутентификации включает проверку учетных данных пользователя
    и верификацию его домена.

    Args:
        login_data: Данные для входа в формате OAuth2 (username и password)
        session: Асинхронная сессия базы данных

    Returns:
        LoginResponse: Объект с JWT токеном доступа и типом токена

    Raises:
        HTTPException: 401 - если пользователь не найден или неверный пароль
        HTTPException: 403 - если пользователь не является regular доменом
    """
    try:
        user = await authenticate_user(session, login_data)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
        )
    except UserNotRegular:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только реальные пользователи могут \
                    авторизоваться и управлять ботфермой"
        )

    settings = get_settings()
    access_token = create_access_token(
        data={"sub": user.login},
        expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    return LoginResponse(access_token=access_token, token_type="bearer")
