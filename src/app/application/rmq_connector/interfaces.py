import abc

from typing import Protocol, Callable, Coroutine

from aio_pika import Channel, Message
from aio_pika.abc import (
    AbstractIncomingMessage,
    ExchangeType,
    AbstractRobustConnection,
    DeliveryMode,
    AbstractExchange,
)
from aio_pika.pool import Pool


class RabbitMQConnectorGateway(Protocol):
    @abc.abstractmethod
    def channel_pool(self) -> Pool[Channel]:
        raise NotImplementedError

    @abc.abstractmethod
    async def publish(
        self, *message_bodies: dict, routing_key: str, exchange_name: str | None = None,
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def consume(
        self, queue_name: str, callback: Callable[[AbstractIncomingMessage], Coroutine],
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_exchange(
        self, name: str, type_: ExchangeType = ExchangeType.TOPIC,
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_queue(self, name: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def bid_queue(
        self, queue_name: str, routing_key: str, exchange_name: str,
    ) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_exchange(self, name: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_queue(self, name: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def shutdown(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_exchange(
        self, channel: Channel, exchange_name: str | None,
    ) -> AbstractExchange:
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_connection(self) -> AbstractRobustConnection:
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_channel(self) -> Channel:
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def _serialize_message(
        body: dict, delivery_mode: DeliveryMode = DeliveryMode.PERSISTENT,
    ) -> Message:
        raise NotImplementedError
