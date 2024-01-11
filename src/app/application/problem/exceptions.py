from dataclasses import dataclass

from src.app.application.common.exceptions import DatabaseGatewayError


class ProblemDatabaseGatewayError(DatabaseGatewayError):
    pass


class ProblemMemberDatabaseGatewayError(DatabaseGatewayError):
    pass


class ProblemStateDatabaseGatewayError(DatabaseGatewayError):
    pass


@dataclass(eq=False)
class ProblemIdNotExists(ProblemDatabaseGatewayError):  # noqa: N818
    id: int

    @property
    def title(self) -> str:
        return f"A problem with id {self.id} does not exist"


@dataclass(eq=False)
class ProblemStateIdNotExists(ProblemStateDatabaseGatewayError):  # noqa: N818
    id: int

    @property
    def title(self) -> str:
        return f"A problem state with id {self.id} does not exist"


@dataclass(eq=False)
class ProblemStateNameNotExists(ProblemStateDatabaseGatewayError):  # noqa: N818
    name: str

    @property
    def title(self) -> str:
        return f"A problem state with name {self.name} does not exist"
