from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from .base import BaseModel

if TYPE_CHECKING:
    from .problem import Problem
    from .user import User
    from .comments import Comment


class ProblemMember(BaseModel):
    __tablename__ = "problem_member"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    problem_id: Mapped[int] = mapped_column(ForeignKey("problem.id"))

    user: Mapped["User"] = relationship(back_populates="user")
    problem: Mapped["Problem"] = relationship(back_populates="problem")
    comments: Mapped[list["Comment"]] = relationship(back_populates="commentator")
