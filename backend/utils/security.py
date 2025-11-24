from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(
        plain_password: str,
        hashed_password: str
) -> bool:
    """
    Проверка соответствия пароля и хеша.

    Args:
        plain_password: Пароль в открытом виде
        hashed_password: Хешированный пароль

    Returns:
        bool: True если пароль верный, иначе False
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Генерация хеша пароля.

    Args:
        password: Пароль в открытом виде

    Returns:
        str: Хешированный пароль
    """
    return pwd_context.hash(password)
