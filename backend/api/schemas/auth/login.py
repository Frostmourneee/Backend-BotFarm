from pydantic import BaseModel, Field


class Login(BaseModel):
    pass


class LoginResponse(BaseModel):
    access_token: str = Field(
        ...,
        description="Токен доступа"
    )
    token_type: str = Field(
        ...,
        description="Тип токена"
    )
