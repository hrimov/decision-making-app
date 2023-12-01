from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from .base import BaseModel, CreatedUpdatedAtMixin


if TYPE_CHECKING:
    from .user import User
    from .stages import ProblemStatement, SuggestionStage, VotingStage, Suggestion
    from .problem_member import ProblemMember


class Problem(CreatedUpdatedAtMixin):
    __tablename__ = "problem"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(20))
    description: Mapped[str]
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    private: Mapped[bool]
    state_id: Mapped[int] = mapped_column(ForeignKey("problem_state.id"))

    state: Mapped["ProblemState"] = relationship(back_populates="problems")
    creator: Mapped["User"] = relationship(back_populates="created_problems")
    problem_members: Mapped[list["ProblemMember"]] = relationship(back_populates="problem")
    problem_statement: Mapped["ProblemStatement"] = relationship(back_populates="problem")
    suggestion_stage: Mapped["SuggestionStage"] = relationship(back_populates="problem")
    suggestions: Mapped[list["Suggestion"]] = relationship(back_populates="problem")
    voting_stage: Mapped["VotingStage"] = relationship(back_populates="problem")


class ProblemState(BaseModel):
    __tablename__ = "problem_state"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    problems: Mapped[list["Problem"]] = relationship(back_populates="state")
