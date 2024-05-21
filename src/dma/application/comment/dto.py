from dataclasses import dataclass
from datetime import datetime
from typing import List, TYPE_CHECKING

from dma.application.common.dto import DTO

if TYPE_CHECKING:
    from dma.application.problem.dto import ProblemMember, ProblemStatement
    from dma.application.stage.dto import Result, Suggestion


@dataclass(frozen=True)
class Comment(DTO):
    id: int
    text: str
    posted: datetime
    problem_member_id: int

    commentator: "ProblemMember"


@dataclass(frozen=True)
class ProblemStatementComment(DTO):
    id: int
    problem_statement_id: int
    parent_comment_id: int

    problem_statement: "ProblemStatement"
    parent: "ProblemStatementComment"
    child_comments: List["ProblemStatementComment"]


@dataclass(frozen=True)
class SuggestionComment(DTO):
    id: int
    suggestion_id: int
    parent_comment_id: int

    suggestion: "Suggestion"
    parent: "SuggestionComment"
    child_comments: List["SuggestionComment"]


@dataclass(frozen=True)
class ResultComment(DTO):
    id: int
    result_id: int
    parent_comment_id: int

    result: "Result"
    parent: "ResultComment"
    child_comments: List["ResultComment"]
