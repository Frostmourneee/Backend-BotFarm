from pydantic import BaseModel, ConfigDict, Field, EmailStr, AwareDatetime
from uuid import UUID
from enum import Enum
from typing import Optional


class EnvironmentEnum(Enum):
    prod = "prod"
    preprod = "preprod"
    stage = "stage"


class DomainEnum(Enum):
    canary = "canary"
    regular = "regular"


class UserCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    login: EmailStr = Field(
        ...,
        min_length=1,
        max_length=255,
        description="E-mail пользователя"
    )
    password: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Пароль в зашифрованном виде"
    )
    project_id: UUID = Field(
        ...,
        description="UUID проекта, к которому прикреплен пользователь"
    )
    env: EnvironmentEnum = Field(
        ...,
        description="Название окружения (prod, preprod, stage)"
    )
    domain: DomainEnum = Field(
        ...,
        description="Тип пользователя (canary, regular)"
    )
    locktime: Optional[AwareDatetime] = Field(
        None,
        description="Время наложения блокировки (TimeStamp)"
    )

class UserCreateResponse(BaseModel):
    message: str = "Пользователь успешно создан"
