from pydantic import BaseModel

class UserLock(BaseModel):
    pass

class UserLockResponse(BaseModel):
    message: str = "Пользователь успешно заблокирован"