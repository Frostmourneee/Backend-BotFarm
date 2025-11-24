from pydantic import BaseModel, Field

from backend.api.schemas.users.base import UserBase


class UserCreate(UserBase):
    pass


class UserCreateResponse(BaseModel):
    message: str = Field(
        "Пользователь успешно создан",
        description="Сообщение об успехе"
    )
