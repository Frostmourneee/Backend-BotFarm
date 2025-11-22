from urllib.parse import urlparse

from fastapi import FastAPI
from uvicorn import run

from backend.config.default import DefaultSettings
from backend.config.utils import get_settings
from backend.api.handlers import list_of_routes


def bind_routes(application: FastAPI, settings: DefaultSettings) -> None:
    """
    Бинд всех путей к приложению
    """
    for route in list_of_routes:
        application.include_router(route, prefix=settings.API_PATH_PREFIX)


def get_app() -> FastAPI:
    """
    Создание инстанса приложения
    """
    description = "Бот-ферма"

    application = FastAPI(
        title="Бот-ферма",
        description=description,
        docs_url="/swagger",
        openapi_url="/openapi",
        version="1.0.0",
    )
    settings = get_settings()
    bind_routes(application, settings)
    application.state.settings = settings
    return application


app = get_app()

if __name__ == "__main__":
    settings_for_application = get_settings()
    run(
        "backend.__main__:app",
        host=urlparse(settings_for_application.APP_HOST).netloc,
        port=settings_for_application.APP_PORT,
        reload=True,
        reload_dirs=["backend"],
        log_level="debug",
    )