from os import environ

from pydantic_settings import BaseSettings, SettingsConfigDict


class DefaultSettings(BaseSettings):
    """
    Класс с настройками приложения по умолчанию
    """

    API_PATH_PREFIX: str = environ.get("API_PATH_PREFIX", "/api/v1")
    APP_HOST: str = environ.get("APP_HOST", "http://0.0.0.0")
    APP_PORT: int = int(environ.get("APP_PORT", 8080))

    POSTGRES_DB_NAME: str = environ.get("POSTGRES_DB_NAME", "postgres")
    POSTGRES_USERNAME: str = environ.get("POSTGRES_USERNAME", "admin")
    POSTGRES_PASSWORD: str = environ.get("POSTGRES_PASSWORD", "pwd")

    # DB_URL: Optional[str] = environ.get("DB_URL")
    # POSTGRES_HOST: str = environ.get("POSTGRES_HOST", "localhost")
    # POSTGRES_PORT: int = int(environ.get("POSTGRES_PORT", "5432")[-4:])

    # SECRET_KEY: str = environ.get("SECRET_KEY")
    # ALGORITHM: str = environ.get("ALGORITHM", "HS256")
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = environ.get(
    #     "ACCESS_TOKEN_EXPIRE_MINUTES", 60)
    #
    # @property
    # def database_settings(self) -> dict:
    #     """
    #     Get all settings for connection with database.
    #     """
    #     return {
    #         "database": self.DB_DATABASE_NAME,
    #         "user": self.DB_USERNAME,
    #         "password": self.DB_PASSWORD,
    #         "host": self.POSTGRES_HOST,
    #         "port": self.POSTGRES_PORT,
    #     }
    #
    # @property
    # def database_uri(self) -> str:
    #     """
    #     Get uri for connection with database.
    #     """
    #     if self.DB_URL:
    #         return self.DB_URL.replace("psycopg2", "asyncpg")
    #     return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
    #         **self.database_settings,
    #     )
    #
    # @property
    # def database_uri_sync(self) -> str:
    #     """
    #     Get uri for connection with database.
    #     """
    #     if self.DB_URL:
    #         return self.DB_URL.replace("asyncpg", "psycopg2")
    #     return "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(
    #         **self.database_settings,
    #     )
    #

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )