from dataclasses import dataclass

from .application import AppConfig
from .database import DatabaseConfig


@dataclass
class Config:
    app_config: AppConfig
    db_config: DatabaseConfig
