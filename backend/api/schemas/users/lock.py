from fastapi import status
from pydantic import BaseModel, Field

class UserLock(BaseModel):
    pass

class UserLockResponse(BaseModel):
    message: str = Field(
        "Пользователь успешно заблокирован",
        description="Сообщение об успехе"
    )

LOCK_RESPONSES = {
    status.HTTP_401_UNAUTHORIZED: {
        "content": {
            "application/json": {
                "example": {"detail": "Не авторизован"}
            }
        }
    },
    status.HTTP_403_FORBIDDEN: {
        "content": {
            "application/json": {
                "example": {"detail": "Доступ только для regular"}
            }
        }
    },
    status.HTTP_404_NOT_FOUND: {
        "content": {
            "application/json": {
                "example": {"detail": "Пользователь не найден"}
            }
        }
    },
}