from dataclasses import dataclass
from typing import List, TYPE_CHECKING

from src.app.application.common.dto import DTO, StartedEndedAtMixin


if TYPE_CHECKING:
    from src.app.application.comment.dto import ResultComment, SuggestionComment
    from src.app.application.problem.dto import Problem


@dataclass(frozen=True)
class SuggestionStage(StartedEndedAtMixin):
    id: int
    problem_id: int

    problem: "Problem"


@dataclass(frozen=True)
class Suggestion(DTO):
    id: int
    title: str
    description: str
    content_path: str | None
    creator_id: int
    problem_id: int

    problem: "Problem"
    suggestion_votes: List["SuggestionVote"]
    comments: List["SuggestionComment"]
    best: "Result"


@dataclass(frozen=True)
class VotingStage(StartedEndedAtMixin):
    id: int
    problem_id: int

    problem: "Problem"
    suggestions_on_vote: List["SuggestionVote"]


@dataclass(frozen=True)
class SuggestionVote(DTO):
    id: int
    voter_id: int
    suggestion_id: int
    voting_id: int

    suggestion: "Suggestion"
    voting: "VotingStage"


@dataclass(frozen=True)
class Result(DTO):
    id: int
    title: str
    suggestion_id: int
    decision: str
    content_path: str | None

    suggestion: "Suggestion"
    comments: List["ResultComment"]



