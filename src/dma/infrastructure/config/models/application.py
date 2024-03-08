from dataclasses import dataclass


@dataclass
class AppConfig:
    host: str
    port: int
    logging_level: str = "DEBUG"
