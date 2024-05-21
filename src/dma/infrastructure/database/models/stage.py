from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from .base import BaseModel, StartedEndedAtMixin

if TYPE_CHECKING:
    from .problem import Problem
    from .comment import ProblemStatementComment, SuggestionComment, ResultComment


class ProblemStatement(BaseModel):
    __tablename__ = "problem_statements"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    content_path: Mapped[str | None]
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"))

    problem: Mapped["Problem"] = relationship(
        back_populates="problem_statement",
    )
    comments: Mapped[list["ProblemStatementComment"]] = relationship(
        back_populates="problem_statement",
    )


class SuggestionStage(StartedEndedAtMixin):
    __tablename__ = "suggestion_stages"

    id: Mapped[int] = mapped_column(primary_key=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"))

    problem: Mapped["Problem"] = relationship(
        back_populates="suggestion_stage",
    )


class Suggestion(BaseModel):
    __tablename__ = "suggestions"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(20))
    description: Mapped[str]
    content_path: Mapped[str | None]
    creator_id: Mapped[int] = mapped_column(ForeignKey("problem_members.id"))
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"))

    problem: Mapped["Problem"] = relationship(
        back_populates="suggestions",
    )
    suggestion_votes: Mapped[list["SuggestionVote"]] = relationship(
        back_populates="suggestion",
    )
    comments: Mapped[list["SuggestionComment"]] = relationship(
        back_populates="suggestion",
    )
    best: Mapped["Result"] = relationship(
        back_populates="suggestion",
    )


class VotingStage(StartedEndedAtMixin):
    __tablename__ = "voting_stages"

    id: Mapped[int] = mapped_column(primary_key=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"))

    problem: Mapped["Problem"] = relationship(
        back_populates="voting_stage",
    )
    suggestions_on_vote: Mapped[list["SuggestionVote"]] = relationship(
        back_populates="voting",
    )


class SuggestionVote(BaseModel):
    __tablename__ = "suggestion_votes"

    id: Mapped[int] = mapped_column(primary_key=True)
    voter_id: Mapped[int] = mapped_column(ForeignKey("problem_members.id"))
    suggestion_id: Mapped[int] = mapped_column(ForeignKey("suggestions.id"))
    voting_id: Mapped[int] = mapped_column(ForeignKey("voting_stages.id"))

    suggestion: Mapped["Suggestion"] = relationship(
        back_populates="suggestion_votes",
    )
    voting: Mapped["VotingStage"] = relationship(
        back_populates="suggestions_on_vote",
    )


class Result(BaseModel):
    __tablename__ = "results"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(20))
    suggestion_id: Mapped[int] = mapped_column(ForeignKey("suggestions.id"))
    decision: Mapped[str]
    content_path: Mapped[str | None]

    suggestion: Mapped["Suggestion"] = relationship(
        back_populates="best",
    )
    comments: Mapped[list["ResultComment"]] = relationship(
        back_populates="result",
    )
