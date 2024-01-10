import configparser
import os

from src.app.infrastructure.config.models import (
    AppConfig,
    Config,
    DatabaseConfig,
    ObjectStorageConfig,
)


DEFAULT_CONFIG_PATH: str = "./config/local.ini"


def load_config(path: str | None = None) -> Config:
    if path is None:
        path = os.getenv("CONFIG_PATH", DEFAULT_CONFIG_PATH)

    parser = configparser.ConfigParser()
    parser.read(path)

    application_data = parser["application"]
    database_data = parser["database"]
    object_storage_data = parser["object_storage"]

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
    object_storage_config = ObjectStorageConfig(
        access_key=object_storage_data.get("access_key"),
        secret_key=object_storage_data.get("secret_key"),
        bucket_name=object_storage_data.get("bucket_name"),
    )

    return Config(application_config, database_config, object_storage_config)
