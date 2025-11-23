from datetime import datetime, UTC, timedelta
import jwt
from jwt.exceptions import InvalidTokenError

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend.business_logic.exceptions import UserNotFound, UserNotRegular
from backend.db.models.user import User
from backend.crud.users.get_by_login import get_user_by_login
from backend.utils.security import verify_password
from backend.config.utils import get_settings
from backend.db.init_db import get_session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")


async def authenticate_user(
        session: AsyncSession,
        login_data: OAuth2PasswordRequestForm
) -> User:
    """
    Аутентифицирует пользователя по логину и паролю
    """
    user = await get_user_by_login(session, login_data.username)
    if not user:
        raise UserNotFound()

    if not verify_password(login_data.password, user.password):
        raise UserNotFound()

    if user.domain != "regular":
        raise UserNotRegular

    return user


def create_access_token(
        data: dict,
        expires_delta: int
) -> str:
    """
    Создает JWT токен
    """
    to_encode = data.copy()
    expire = datetime.now(tz=UTC) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})

    settings = get_settings()
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session)
) -> User:
    """
    Получает текущего аутентифицированного пользователя по JWT токену
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Невалидный токен",
    )

    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        login = payload.get("sub")
        if not login:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = await get_user_by_login(session, login)
    if not user:
        raise credentials_exception

    return user

async def require_regular_user(
        user: User = Depends(get_current_user)
) -> User:
    """
    Пользоваться ботофермой могут только настоящие пользователи (разработчики)
    """
    if user.domain != "regular":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ только для regular"
        )

    return user