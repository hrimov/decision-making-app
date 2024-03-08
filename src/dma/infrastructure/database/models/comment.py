from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from .base import BaseModel

if TYPE_CHECKING:
    from .problem_member import ProblemMember
    from .stage import ProblemStatement, Suggestion, Result


class Comment(BaseModel):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(100))
    posted: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    problem_member_id: Mapped[int] = mapped_column(ForeignKey("problem_members.id"))

    commentator: Mapped["ProblemMember"] = relationship(
        back_populates="comments",
    )


class ProblemStatementComment(BaseModel):
    __tablename__ = "problem_statement_comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    problem_statement_id: Mapped[int] = mapped_column(
        ForeignKey("problem_statements.id"),
    )
    parent_comment_id: Mapped[int] = mapped_column(
        ForeignKey("problem_statement_comments.id"),
    )

    problem_statement: Mapped["ProblemStatement"] = relationship(
        back_populates="comments",
    )
    parent: Mapped["ProblemStatementComment"] = relationship(
        back_populates="child_comments", remote_side=[id],
    )
    child_comments: Mapped[list["ProblemStatementComment"]] = relationship(
        back_populates="parent",
    )


class SuggestionComment(BaseModel):
    __tablename__ = "suggestion_comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    suggestion_id: Mapped[int] = mapped_column(ForeignKey("suggestions.id"))
    parent_comment_id: Mapped[int] = mapped_column(ForeignKey("suggestion_comments.id"))

    suggestion: Mapped["Suggestion"] = relationship(
        back_populates="comments",
    )
    parent: Mapped["SuggestionComment"] = relationship(
        back_populates="child_comments", remote_side=[id],
    )
    child_comments: Mapped[list["SuggestionComment"]] = relationship(
        back_populates="parent",
    )


class ResultComment(BaseModel):
    __tablename__ = "result_comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    result_id: Mapped[int] = mapped_column(ForeignKey("results.id"))
    parent_comment_id: Mapped[int] = mapped_column(ForeignKey("result_comments.id"))

    result: Mapped["Result"] = relationship(
        back_populates="comments",
    )
    parent: Mapped["ResultComment"] = relationship(
        back_populates="child_comments", remote_side=[id],
    )
    child_comments: Mapped[list["ResultComment"]] = relationship(
        back_populates="parent",
    )
