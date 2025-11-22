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

    BOT_POSTGRES_DB: str = Field(default="botfarm-postgres")
    BOT_POSTGRES_USER: str = Field(default="admin")
    BOT_POSTGRES_PASSWORD: str = Field(default="pwd")

    BOT_POSTGRES_HOST: str = Field(default="botfarm-postgres")
    BOT_POSTGRES_PORT: int = Field(default=5432)

    # SECRET_KEY: str = environ.get("SECRET_KEY")
    # ALGORITHM: str = environ.get("ALGORITHM", "HS256")
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = environ.get(
    #     "ACCESS_TOKEN_EXPIRE_MINUTES", 60)

    @property
    def database_settings(self) -> dict:
        return {
            "db_name": self.BOT_POSTGRES_DB,
            "user": self.BOT_POSTGRES_USER,
            "pwd": self.BOT_POSTGRES_PASSWORD,
            "host": self.BOT_POSTGRES_HOST,
            "port": self.BOT_POSTGRES_PORT,
        }

    @property
    def database_uri(self) -> str:
        """
        URI для асинхронного соединения
        """
        return (
            "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
            .format(**self.database_settings)
        )
