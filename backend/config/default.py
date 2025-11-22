from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class DefaultSettings(BaseSettings):
    """
    Класс с настройками приложения по умолчанию
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    API_PATH_PREFIX: str = Field(default="/api/v1")
    APP_HOST: str = Field(default="http://0.0.0.0")
    APP_PORT: int = Field(default=8080)

    POSTGRES_DB_NAME: str = Field(default="postgres")
    POSTGRES_USERNAME: str = Field(default="admin")
    POSTGRES_PASSWORD: str = Field(default="pwd")

    POSTGRES_HOST: str = Field()
    POSTGRES_PORT: int = Field(default=5432)

    # SECRET_KEY: str = environ.get("SECRET_KEY")
    # ALGORITHM: str = environ.get("ALGORITHM", "HS256")
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = environ.get(
    #     "ACCESS_TOKEN_EXPIRE_MINUTES", 60)

    @property
    def database_settings(self) -> dict:
        return {
            "database": self.POSTGRES_DB_NAME,
            "user": self.POSTGRES_USERNAME,
            "password": self.POSTGRES_PASSWORD,
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT,
        }

    @property
    def database_uri(self) -> str:
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )
