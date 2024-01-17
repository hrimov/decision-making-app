import asyncio
from uuid import uuid4

import pytest
from aio_pika import Queue, Exchange
from aio_pika.abc import AbstractIncomingMessage
from aiormq import ChannelNotFoundEntity

from src.app.infrastructure.rmq_connector.gateway import RabbitMQConnectorGatewayImpl


@pytest.mark.order(1)
async def test_declare_exchange(rmq_connector_gateway: RabbitMQConnectorGatewayImpl):
    exchange_name = str(uuid4())
    await rmq_connector_gateway.create_exchange(exchange_name)

    async with rmq_connector_gateway.channel_pool.acquire() as channel:
        exchange = await channel.get_exchange(name=exchange_name, ensure=True)
    assert exchange.name == exchange_name


@pytest.mark.order(2)
async def test_declare_queue(rmq_connector_gateway: RabbitMQConnectorGatewayImpl):
    queue_name = str(uuid4())
    await rmq_connector_gateway.create_queue(queue_name)

    async with rmq_connector_gateway.channel_pool.acquire() as channel:
        queue = await channel.get_queue(name=queue_name, ensure=True)
    assert queue.name == queue_name


@pytest.mark.order(3)
async def test_bid_queue(
    rmq_connector_gateway: RabbitMQConnectorGatewayImpl,
    queue: Queue,
    exchange: Exchange,
):
    bis_success = await rmq_connector_gateway.bid_queue(
        queue_name=queue.name,
        exchange_name=exchange.name,
        routing_key="some-routing-key",
    )
    assert bis_success is True


@pytest.mark.order(4)
async def test_publish_message(
    rmq_connector_gateway: RabbitMQConnectorGatewayImpl, exchange: Exchange,
):
    message = {"some": "some_value"}
    await rmq_connector_gateway.publish(
        message, routing_key="some_key", exchange_name=exchange.name,
    )


@pytest.mark.order(5)
async def test_publish_not_exist_exchange(
    rmq_connector_gateway: RabbitMQConnectorGatewayImpl,
):
    exchange_name = "not_real_exchange"
    with pytest.raises(ChannelNotFoundEntity) as e:
        await rmq_connector_gateway.publish(
            {"some": "value"}, routing_key="some_key", exchange_name=exchange_name,
        )

    assert str(e.value) == f"NOT_FOUND - no exchange '{exchange_name}' in vhost '/'"


@pytest.mark.order(6)
async def test_consume_message(
    rmq_connector_gateway: RabbitMQConnectorGatewayImpl,
    queue: Queue,
    exchange: Exchange,
):
    routing_key = str(uuid4())
    message_body = {"some": "some_value"}
    consumed = False
    await rmq_connector_gateway.bid_queue(
        queue_name=queue.name, routing_key=routing_key, exchange_name=exchange.name,
    )
    await rmq_connector_gateway.publish(
        message_body, routing_key=routing_key, exchange_name=exchange.name,
    )

    async def consume_callback(message: AbstractIncomingMessage) -> bool:
        nonlocal consumed
        async with message.process():
            assert message.routing_key == routing_key
            assert message.exchange == exchange.name
            consumed = True
            await message.ack()
            return True

    await rmq_connector_gateway.consume(
        queue_name=queue.name, callback=consume_callback,
    )

    await asyncio.sleep(0.001)
    assert consumed is True


@pytest.mark.order(7)
async def test_consume_not_exist_queue(
    rmq_connector_gateway: RabbitMQConnectorGatewayImpl,
):
    queue_name = "NotExistName"
    with pytest.raises(ChannelNotFoundEntity) as e:
        await rmq_connector_gateway.consume(queue_name=queue_name, callback=lambda m: m)  # type: ignore

    assert str(e.value) == f"NOT_FOUND - no queue '{queue_name}' in vhost '/'"
