from typing import Generator, AsyncGenerator
from uuid import uuid4

from testcontainers.rabbitmq import RabbitMqContainer # type: ignore[import-untyped]

import pytest
import pytest_asyncio

from src.app.infrastructure.config.models import MessageQueueConfig
from src.app.infrastructure.message_queue.gateway import MessageQueueGatewayImpl


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
async def message_queue_gateway(
        rmq_container: RabbitMqContainer,
) -> AsyncGenerator[MessageQueueGatewayImpl, None]:
    config = MessageQueueConfig(
        host=rmq_container.get_container_host_ip(),
        port=rmq_container.get_exposed_port(5672),
    )
    gateway = MessageQueueGatewayImpl(config)
    yield gateway
    await gateway.shutdown()

@pytest.fixture()
async def queue(message_queue_gateway: MessageQueueGatewayImpl):
    queue_name = str(uuid4())
    await message_queue_gateway.create_queue(queue_name)

    async with message_queue_gateway.channel_pool.acquire() as channel:
        yield await channel.get_queue(name=queue_name, ensure=True)

    await message_queue_gateway.delete_queue(queue_name)


@pytest.fixture()
async def exchange(message_queue_gateway: MessageQueueGatewayImpl):
    exchange_name = str(uuid4())
    await message_queue_gateway.create_exchange(exchange_name)

    async with message_queue_gateway.channel_pool.acquire() as channel:
        yield await channel.get_exchange(name=exchange_name, ensure=True)

    await message_queue_gateway.delete_exchange(exchange_name)
