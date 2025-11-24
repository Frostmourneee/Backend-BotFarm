from pydantic import BaseModel, Field


class UserUnlock(BaseModel):
    pass


class UserUnlockResponse(BaseModel):
    message: str = Field(
        "Пользователь успешно разблокирован",
        description="Сообщение об успехе"
    )
