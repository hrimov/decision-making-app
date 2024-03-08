import abc

from typing import Protocol

from dma.application.common.pagination import Pagination
from dma.application.user import dto
from dma.application.user.filters import UserFilters


class UserGateway(Protocol):
    @abc.abstractmethod
    async def get_user_by_id(self, id_: int) -> dto.User:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_user_by_nickname(self, nickname: str) -> dto.User:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_users(
            self, filters: UserFilters, pagination: Pagination,
    ) -> dto.Users:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_user(self, user_dto: dto.User) -> dto.User:
        raise NotImplementedError

    @abc.abstractmethod
    async def update_user(self, user_dto: dto.User) -> dto.User:
        raise NotImplementedError
