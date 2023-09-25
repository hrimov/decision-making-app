from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    host: str
    port: int
    database: str
    user: str
    password: str
    echo: bool
