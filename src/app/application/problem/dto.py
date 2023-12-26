from dataclasses import dataclass
from typing import List, TypeAlias, TYPE_CHECKING

from src.app.application.common.dto import DTO
from src.app.application.common.pagination import PaginatedItems


if TYPE_CHECKING:
    from src.app.application.comment.dto import Comment, ProblemStatementComment
    from src.app.application.stage.dto import Suggestion, SuggestionStage, VotingStage
    from src.app.application.user.dto import User


@dataclass(frozen=True)
class Problem(DTO):
    id: int
    title: str
    description: str
    creator_id: int
    private: bool
    state_id: int


@dataclass(frozen=True)
class ProblemCreate(DTO):
    title: str
    description: str
    creator_id: int
    private: bool
    state_id: int


@dataclass(frozen=True)
class ProblemUpdate(DTO):
    id: int
    title: str | None = None
    description: str | None = None
    private: bool | None = None
    state_id: int | None = None


@dataclass(frozen=True)
class ProblemWithRelations(Problem):
    state: "ProblemState"
    creator: "User"
    problem_members: List["ProblemMember"]
    suggestion_stage: "SuggestionStage"
    suggestions: List["Suggestion"]
    voting_stage: "VotingStage"


@dataclass(frozen=True)
class ProblemMember(DTO):
    id: int
    user_id: int
    problem_id: int

    user: "User"
    problem: "Problem"
    comments: List["Comment"]


@dataclass(frozen=True)
class ProblemState(DTO):
    id: int
    name: str


@dataclass(frozen=True)
class ProblemStateCreate(DTO):
    name: str


@dataclass(frozen=True)
class ProblemStateWithRelations(ProblemState):
    problems: List["Problem"]


@dataclass(frozen=True)
class ProblemStatement(DTO):
    id: int
    description: str
    content_path: str | None
    problem_id: int

    problem: "Problem"
    comments: List["ProblemStatementComment"]


Problems: TypeAlias = PaginatedItems[Problem]
ProblemStates: TypeAlias = PaginatedItems[ProblemState]
