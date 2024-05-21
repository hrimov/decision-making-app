from dataclasses import dataclass


@dataclass
class MessageQueueConfig:
    host: str
    port: str
    username: str = "guest"
    password: str = "guest"
    connector_prefix: str = "amqp"

    # options that are not usable in the full url
    connection_pool_max_size: int = 3
    channel_pool_max_size: int = 15
    batch_size: int = 200
    default_exchange_name: str = "decision_making_app"

    @property
    def full_url(self) -> str:
        return "{}://{}:{}@{}:{}".format(
            self.connector_prefix,
            self.username, self.password,
            self.host, self.port,
        )
