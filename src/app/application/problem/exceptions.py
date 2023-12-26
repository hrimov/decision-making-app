from dataclasses import dataclass

from src.app.application.common.exceptions import GatewayError


class ProblemGatewayError(GatewayError):
    pass


class ProblemMemberGatewayError(GatewayError):
    pass


class ProblemStateGatewayError(GatewayError):
    pass


@dataclass(eq=False)
class ProblemIdNotExists(ProblemGatewayError):
    id: int

    @property
    def title(self) -> str:
        return f"A problem with id {self.id} does not exist"


@dataclass(eq=False)
class ProblemStateIdNotExists(ProblemStateGatewayError):
    id: int

    @property
    def title(self) -> str:
        return f"A problem state with id {self.id} does not exist"


@dataclass(eq=False)
class ProblemStateNameNotExists(ProblemStateGatewayError):
    name: str

    @property
    def title(self) -> str:
        return f"A problem state with name {self.name} does not exist"
