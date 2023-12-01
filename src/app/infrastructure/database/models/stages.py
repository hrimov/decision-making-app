from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from .base import BaseModel, StartedEndsAtMixin

if TYPE_CHECKING:
    from .problem import Problem
    from .comments import ProblemStatementComment, SuggestionComment, ResultComment


class ProblemStatement(BaseModel):
    __tablename__ = "problem_statement"
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    content_path: Mapped[str | None]
    problem_id: Mapped[int] = mapped_column(ForeignKey("problem.id"))

    problem: Mapped["Problem"] = relationship(back_populates="problem_statement")
    comments: Mapped[list["ProblemStatementComment"]] = relationship(back_populates="problem_statement")


class SuggestionStage(StartedEndsAtMixin):
    __tablename__ = "suggestion_stage"
    id: Mapped[int] = mapped_column(primary_key=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey("problem.id"))

    problem: Mapped["Problem"] = relationship(back_populates="suggestion_stage")


class Suggestion(BaseModel):
    __tablename__ = "suggestion"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(20))
    description: Mapped[str]
    content_path: Mapped[str | None]
    creator_id: Mapped[int] = mapped_column(ForeignKey("problem_member.id"))
    problem_id: Mapped[int] = mapped_column(ForeignKey("problem.id"))

    problem: Mapped["Problem"] = relationship(back_populates="suggestions")
    suggestion_votes: Mapped[list["SuggestionVote"]] = relationship(back_populates="suggestion")
    comments: Mapped[list["SuggestionComment"]] = relationship(back_populates="suggestion")
    best: Mapped["Result"] = relationship(back_populates="suggestion")


class VotingStage(StartedEndsAtMixin):
    __tablename__ = "voting_stage"
    id: Mapped[int] = mapped_column(primary_key=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey("problem.id"))

    problem: Mapped["Problem"] = relationship(back_populates="voting_stage")
    suggestions_on_vote: Mapped[list["SuggestionVote"]] = relationship(back_populates="voting")


class SuggestionVote(BaseModel):
    __tablename__ = "suggestion_vote"
    id: Mapped[int] = mapped_column(primary_key=True)
    voter_id: Mapped[int] = mapped_column(ForeignKey("problem_member.id"))
    suggestion_id: Mapped[int] = mapped_column(ForeignKey("suggestion.id"))
    voting_id: Mapped[int] = mapped_column(ForeignKey("voting_stage.id"))

    suggestion: Mapped["Suggestion"] = relationship(back_populates="suggestion_votes")
    voting: Mapped["VotingStage"] = relationship(back_populates="suggestions_on_vote")


class Result(BaseModel):
    __tablename__ = "result"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(20))
    suggestion_id: Mapped[int] = mapped_column(ForeignKey("suggestion.id"))
    decision: Mapped[str]
    content_path: Mapped[str | None]

    suggestion: Mapped["Suggestion"] = relationship(back_populates="best")
    comments: Mapped[list["ResultComment"]] = relationship("result")



