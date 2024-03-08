import configparser
import os

from dma.infrastructure.config.models import (
    AppConfig,
    Config,
    DatabaseConfig,
    ObjectStorageConfig,
    MessageQueueConfig,
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
    message_queue_data = parser["message_queue"]

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
    message_queue_config = MessageQueueConfig(
        host=message_queue_data.get("host"),
        port=message_queue_data.get("port"),
        username=message_queue_data.get("username"),
        password=message_queue_data.get("password"),
        connection_pool_max_size=message_queue_data.getint("connection_pool_max_size"),
        channel_pool_max_size=message_queue_data.getint("channel_pool_max_size"),
        default_exchange_name=message_queue_data.get("default_exchange_name"),
    )

    return Config(
        application_config,
        database_config,
        object_storage_config,
        message_queue_config,
    )
