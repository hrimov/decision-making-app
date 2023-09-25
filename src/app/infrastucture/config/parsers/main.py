import configparser
import os

from src.app.infrastucture.config.models import (
    AppConfig,
    Config,
    DatabaseConfig,
)


DEFAULT_CONFIG_PATH: str = "./config/local.ini"


def load_config(path: str | None = None) -> Config:
    if path is None:
        path = os.getenv("CONFIG_PATH", DEFAULT_CONFIG_PATH)

    parser = configparser.ConfigParser()
    parser.read(path)

    application_data, database_data = parser["application"], parser["database"]

    application_config = AppConfig(
        host=application_data.get("host"),
        port=application_data.getint("port"),
        logging_level=application_data.get("logging_level"),
    )
    database_config = DatabaseConfig(
        host=database_data.get("host"),
        port=database_data.getint("port"),
        database=database_data.get("database"),
        user=database_data.get("user"),
        password=database_data.get("password"),
        echo=database_data.getboolean("echo"),
    )

    return Config(application_config, database_config)
