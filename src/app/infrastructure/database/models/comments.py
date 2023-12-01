from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from .base import BaseModel

if TYPE_CHECKING:
    from .problem_member import ProblemMember
    from .stages import ProblemStatement, Suggestion, Result


class Comment(BaseModel):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(100))
    posted: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    problem_member_id: Mapped[int] = mapped_column(ForeignKey("problem_member.id"))

    commentator: Mapped["ProblemMember"] = relationship(back_populates="comments")


class ProblemStatementComment(BaseModel):
    __tablename__ = "problem_statement_comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    problem_statement_id: Mapped[int] = mapped_column(ForeignKey("problem_statement.id"))
    parent_comment_id: Mapped[int] = mapped_column(ForeignKey("problem_statement_comment.id"))

    problem_statement: Mapped["ProblemStatement"] = relationship("comments")
    parent: Mapped["ProblemStatementComment"] = relationship(back_populates="child_comments", remote_side=[id])
    child_comments: Mapped[list["ProblemStatementComment"]] = relationship(back_populates="parent")


class SuggestionComment(BaseModel):
    __tablename__ = "suggestion_comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    suggestion_id: Mapped[int] = mapped_column(ForeignKey("suggestion.id"))
    parent_comment_id: Mapped[int] = mapped_column(ForeignKey("suggestion_comment.id"))

    suggestion: Mapped["Suggestion"] = relationship("comments")
    parent: Mapped["SuggestionComment"] = relationship(back_populates="child_comments", remote_side=[id])
    child_comments: Mapped[list["SuggestionComment"]] = relationship(back_populates="parent")


class ResultComment(BaseModel):
    __tablename__ = "suggestion_comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    result_id: Mapped[int] = mapped_column(ForeignKey("result.id"))
    parent_comment_id: Mapped[int] = mapped_column(ForeignKey("result_comment.id"))

    result: Mapped["Result"] = relationship("comments")
    parent: Mapped["ResultComment"] = relationship(back_populates="child_comments", remote_side=[id])
    child_comments: Mapped[list["ResultComment"]] = relationship(back_populates="parent")
