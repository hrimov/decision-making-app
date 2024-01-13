import logging

from src.app.infrastructure.config.models.application import AppConfig
from src.app.infrastructure.log.formatters import MainConsoleFormatter


DEFAULT_LOGGING_LEVEL: int = logging.INFO


def configure_logging(config: AppConfig) -> None:
    if config.logging_level:
        logging_level: int = logging.getLevelName(config.logging_level)
    else:
        logging_level = DEFAULT_LOGGING_LEVEL

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_level)
    console_handler.setFormatter(MainConsoleFormatter())

    logging.basicConfig(handlers=[console_handler], level=logging_level)
