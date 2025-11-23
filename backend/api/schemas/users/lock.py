from pydantic import BaseModel, Field

class UserLock(BaseModel):
    pass

class UserLockResponse(BaseModel):
    message: str = Field(
        "Пользователь успешно заблокирован",
        description="Сообщение об успехе"
    )