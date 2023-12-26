from typing import TYPE_CHECKING

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from .base import CreatedUpdatedAtMixin

if TYPE_CHECKING:
    from .problem import Problem
    from .problem_member import ProblemMember


class User(CreatedUpdatedAtMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(20))
    fullname: Mapped[str]
    password: Mapped[str]
    email: Mapped[str]
    photo_path: Mapped[str | None]
    reputation: Mapped[int] = mapped_column(Integer(), default=0)

    created_problems: Mapped[list["Problem"]] = relationship(back_populates="creator")
    member_of: Mapped[list["ProblemMember"]] = relationship(back_populates="user")
