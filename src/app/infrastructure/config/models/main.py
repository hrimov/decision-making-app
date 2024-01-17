from dataclasses import dataclass

from .application import AppConfig
from .database import DatabaseConfig
from .object_storage import ObjectStorageConfig
from .rmq_connector import RabbitMQConnectorConfig


@dataclass
class Config:
    app_config: AppConfig
    db_config: DatabaseConfig
    storage_config: ObjectStorageConfig
    rmq_connector_config: RabbitMQConnectorConfig
