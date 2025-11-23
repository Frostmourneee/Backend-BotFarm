from pydantic import BaseModel

from backend.api.schemas.users.base import UserBase


class UserCreate(UserBase):
    pass

class UserCreateResponse(BaseModel):
    message: str = "Пользователь успешно создан"
