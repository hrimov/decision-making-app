from typing import Generator, AsyncGenerator
from uuid import uuid4

from testcontainers.rabbitmq import RabbitMqContainer  # type: ignore[import-untyped]

import pytest
import pytest_asyncio

from src.app.infrastructure.config.models import RabbitMQConnectorConfig
from src.app.infrastructure.rmq_connector.gateway import RabbitMQConnectorGatewayImpl


@pytest.fixture(scope="session")
def rmq_container() -> Generator[RabbitMqContainer, None, None]:
    rabbitmq_container = RabbitMqContainer(
        username="guest",
        password="guest",
    )
    try:
        rabbitmq_container.start()
        yield rabbitmq_container
    finally:
        rabbitmq_container.stop()


@pytest_asyncio.fixture()
async def rmq_connector_gateway(
    rmq_container: RabbitMqContainer,
) -> AsyncGenerator[RabbitMQConnectorGatewayImpl, None]:
    config = RabbitMQConnectorConfig(
        host=rmq_container.get_container_host_ip(),
        port=rmq_container.get_exposed_port(5672),
    )
    gateway = RabbitMQConnectorGatewayImpl(config)
    yield gateway
    await gateway.shutdown()


@pytest.fixture()
async def queue(rmq_connector_gateway: RabbitMQConnectorGatewayImpl):
    queue_name = str(uuid4())
    await rmq_connector_gateway.create_queue(queue_name)

    async with rmq_connector_gateway.channel_pool.acquire() as channel:
        yield await channel.get_queue(name=queue_name, ensure=True)

    await rmq_connector_gateway.delete_queue(queue_name)


@pytest.fixture()
async def exchange(rmq_connector_gateway: RabbitMQConnectorGatewayImpl):
    exchange_name = str(uuid4())
    await rmq_connector_gateway.create_exchange(exchange_name)

    async with rmq_connector_gateway.channel_pool.acquire() as channel:
        yield await channel.get_exchange(name=exchange_name, ensure=True)

    await rmq_connector_gateway.delete_exchange(exchange_name)
