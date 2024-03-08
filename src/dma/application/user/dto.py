from dataclasses import dataclass
from typing import List, TypeAlias, TYPE_CHECKING

from dma.application.common.dto import DTO
from dma.application.common.pagination import PaginatedItems


if TYPE_CHECKING:
    from dma.application.problem.dto import Problem, ProblemMember


@dataclass(frozen=True)
class User(DTO):
    id: int
    nickname: str
    fullname: str
    email: str
    photo_path: str | None
    reputation: int


@dataclass(frozen=True)
class UserWithPassword(User):
    password: str


@dataclass(frozen=True)
class UserCreate(DTO):
    nickname: str
    fullname: str
    email: str
    password: str


@dataclass(frozen=True)
class UserUpdate(DTO):
    id: int
    fullname: str | None = None
    email: str | None = None
    photo_path: str | None = None


@dataclass(frozen=True)
class UserWithRelations(User):
    problems_created: List["Problem"]
    member_of: List["ProblemMember"]


Users: TypeAlias = PaginatedItems[User]
