import asyncio
from typing import Callable, Coroutine

from aio_pika import Channel, connect_robust, Connection, ExchangeType, Message
from aio_pika.abc import (
    AbstractExchange,
    AbstractIncomingMessage,
    AbstractRobustConnection,
    DeliveryMode,
)
from aio_pika.pool import Pool
import orjson

from .iterables import batched
from src.app.infrastructure.config.models import RabbitMQConnectorConfig
from src.app.application.rmq_connector.interfaces import RabbitMQConnectorGateway


class RabbitMQConnectorGatewayImpl(RabbitMQConnectorGateway):
    BATCH_SIZE: int = 200

    def __init__(self, settings: RabbitMQConnectorConfig):
        self._settings = settings
        self._connection_pool: Pool[Connection] = Pool(
            self._get_connection,
            max_size=settings.connection_pool_max_size,
        )
        self._channel_pool: Pool[Channel] = Pool(
            self._get_channel,
            max_size=settings.channel_pool_max_size,
        )
        self._default_exchange_name = settings.default_exchange_name

    @property
    def channel_pool(self) -> Pool[Channel]:  # type: ignore
        return self._channel_pool

    async def publish(
        self,
        *message_bodies: dict,
        routing_key: str,
        exchange_name: str | None = None,
    ) -> None:
        async with self._channel_pool.acquire() as channel:
            exchange = await self._get_exchange(
                channel,
                exchange_name=exchange_name or self._default_exchange_name,
            )

            messages = (self._serialize_message(m) for m in message_bodies)
            for messages_batch in batched(
                messages,
                RabbitMQConnectorGatewayImpl.BATCH_SIZE,
            ):
                tasks = [
                    exchange.publish(message=m, routing_key=routing_key)
                    for m in messages_batch
                ]
                await asyncio.gather(*tasks)

    async def consume(
        self,
        queue_name: str,
        callback: Callable[[AbstractIncomingMessage], Coroutine],
    ) -> None:
        async with self._channel_pool.acquire() as channel:
            queue = await channel.get_queue(queue_name, ensure=True)
            await queue.consume(callback, exclusive=True)  # type: ignore

    async def create_exchange(
        self,
        name: str,
        type_: ExchangeType = ExchangeType.TOPIC,
    ) -> None:
        async with self._channel_pool.acquire() as channel:
            await channel.declare_exchange(name, type_)

    async def create_queue(self, name: str) -> None:
        async with self._channel_pool.acquire() as channel:
            await channel.declare_queue(name)

    async def bid_queue(
        self,
        queue_name: str,
        routing_key: str,
        exchange_name: str,
    ) -> bool:
        async with self._channel_pool.acquire() as channel:
            queue = await channel.get_queue(queue_name)
            exchange = await self._get_exchange(channel, exchange_name=exchange_name)
            result = await queue.bind(exchange=exchange, routing_key=routing_key)
        return result.name == "Queue.BindOk"

    async def delete_exchange(self, name: str) -> None:
        async with self._channel_pool.acquire() as channel:
            await channel.exchange_delete(name)

    async def delete_queue(self, name: str) -> None:
        async with self._channel_pool.acquire() as channel:
            await channel.queue_delete(name)

    async def shutdown(self) -> None:
        await self._channel_pool.close()
        await self._connection_pool.close()

    @staticmethod
    def _serialize_message(
        body: dict,
        delivery_mode: DeliveryMode = DeliveryMode.PERSISTENT,
    ) -> Message:
        return Message(body=orjson.dumps(body), delivery_mode=delivery_mode)

    async def _get_exchange(
        self,
        channel: Channel,
        exchange_name: str | None,
    ) -> AbstractExchange:
        exchange_name = exchange_name or self._default_exchange_name
        return await channel.get_exchange(name=exchange_name, ensure=True)

    async def _get_connection(self) -> AbstractRobustConnection:
        return await connect_robust(self._settings.full_url())

    async def _get_channel(self) -> Channel:
        async with self._connection_pool.acquire() as connection:
            return await connection.channel()  # type: ignore
