from fastapi import status
from pydantic import BaseModel, Field, AwareDatetime
from uuid import UUID

from backend.api.schemas.users.base import UserBase

class UserGetAll(BaseModel):
    pass

class UserGetAllResponse(UserBase):
    id: UUID = Field(
        ...,
        description="UUID пользователя"
    )
    dt_created: AwareDatetime = Field(
        ...,
        description="Время появления записи (TimeStamp)"
    )
    locktime: AwareDatetime | None = Field(
        None,
        description="Время наложения блокировки (TimeStamp)"
    )

GET_ALL_RESPONSES = {
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
}
