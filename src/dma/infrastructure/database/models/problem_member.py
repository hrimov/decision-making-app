from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from .base import BaseModel

if TYPE_CHECKING:
    from .problem import Problem
    from .user import User
    from .comment import Comment


class ProblemMember(BaseModel):
    __tablename__ = "problem_members"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"))

    user: Mapped["User"] = relationship(back_populates="member_of")
    problem: Mapped["Problem"] = relationship(back_populates="problem_members")
    comments: Mapped[list["Comment"]] = relationship(back_populates="commentator")
