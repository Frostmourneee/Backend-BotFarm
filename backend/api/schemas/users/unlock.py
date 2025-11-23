from pydantic import BaseModel

class UserUnlock(BaseModel):
    pass

class UserUnlockResponse(BaseModel):
    message: str = "Пользователь успешно разблокирован"