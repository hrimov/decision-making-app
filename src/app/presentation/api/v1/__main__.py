import logging

import uvicorn
from fastapi import FastAPI

from src.app.infrastructure.config.models import AppConfig, Config
from src.app.infrastructure.config.parsers.main import load_config
from src.app.infrastructure.log.main import configure_logging
from src.app.presentation.api.v1 import controllers, middlewares, providers
from src.app.presentation.api.v1.factory import create_fastapi_app


logger = logging.getLogger(__name__)


def main(config: Config) -> FastAPI:
    configure_logging(config.app_config)

    logger.warning("Config loaded. Launching application...")

    app: FastAPI = create_fastapi_app()
    controllers.setup(app=app)
    middlewares.setup(app=app)
    providers.setup(app=app)

    return app


def run() -> None:
    config: Config = load_config()
    app = main(config)
    app_config: AppConfig = config.app_config

    uvicorn_config = uvicorn.Config(
        app=app,
        host=app_config.host,
        port=app_config.port,
        log_level=app_config.logging_level.lower(),
        log_config=None,
        reload=True,
    )
    server = uvicorn.Server(config=uvicorn_config)
    server.run()


if __name__ == "__main__":
    run()
