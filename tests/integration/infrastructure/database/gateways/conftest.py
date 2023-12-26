import pytest

from src.app.application.problem.dto import ProblemCreate
from src.app.application.user.dto import UserCreate


@pytest.fixture
def problem_to_create() -> ProblemCreate:
    return ProblemCreate(
        title="title",
        description="description",
        creator_id=1,
        private=True,
        state_id=1,
    )


@pytest.fixture
def user_to_create() -> UserCreate:
    return UserCreate(
        nickname="nickname",
        fullname="fullname",
        email="email",
        password="pass",
    )
