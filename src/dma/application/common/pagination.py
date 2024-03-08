from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Generic, List, TypeVar

from dma.application.common.dto import DTO


Item = TypeVar("Item")


class SortOrder(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class Pagination:
    pass


class PaginationResult(ABC):
    @classmethod
    @abstractmethod
    def from_pagination(cls, pagination: Pagination, total: int) -> "PaginationResult":
        raise NotImplementedError


@dataclass(frozen=True)
class LimitOffsetPagination(Pagination):
    limit: int | None = None
    offset: int | None = None
    order: SortOrder = SortOrder.ASC


@dataclass(frozen=True)
class LimitOffsetPaginationResult(DTO, PaginationResult):
    limit: int | None
    offset: int | None
    order: SortOrder
    total: int

    @classmethod
    def from_pagination(
            cls,
            pagination: LimitOffsetPagination,  # type: ignore[override]
            total: int,
    ) -> "LimitOffsetPaginationResult":
        return cls(
            offset=pagination.offset,
            limit=pagination.limit,
            order=pagination.order,
            total=total,
        )


@dataclass(frozen=True)
class PaginatedItems(DTO, Generic[Item]):
    data: List[Item]
    pagination: LimitOffsetPaginationResult
