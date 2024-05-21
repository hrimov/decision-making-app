import abc
import io

from typing import Callable, Protocol


class ObjectStorageGateway(Protocol):
    @abc.abstractmethod
    async def upload_file(self, file_path: str, name: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def upload_file_object(self, file_object: io.BytesIO, name: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_object(self, name: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_all_objects(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_file_presigned_url(self, name: str, expires_in: int) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_file_object(self, name: str) -> io.BytesIO:
        raise NotImplementedError


class MessageQueueGateway(Protocol):
    @abc.abstractmethod
    async def publish(
            self,
            *message_bodies: dict,
            routing_key: str,
            exchange_name: str | None = None,
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def consume(
            self,
            queue_name: str,
            callback: Callable,
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_queue(self, name: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_queue(self, name: str) -> None:
        raise NotImplementedError
