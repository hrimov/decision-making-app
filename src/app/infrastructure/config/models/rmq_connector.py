from dataclasses import dataclass


@dataclass
class RabbitMQConnectorConfig:
    host: str
    port: str
    username: str = "guest"
    password: str = "guest"
    connection_pool_max_size: int = 3
    channel_pool_max_size: int = 15
    default_exchange_name: str = "decision_making_app"

    def full_url(self) -> str:
        return f"amqp://{self.username}:{self.password}@{self.host}:{self.port}"
