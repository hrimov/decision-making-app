from dataclasses import dataclass

from src.app.application.common.exceptions import GatewayError


class UserGatewayError(GatewayError):
    pass


@dataclass(eq=False)
class UserIdNotExists(UserGatewayError):
    id: int

    @property
    def title(self) -> str:
        return f"A user with id {self.id} does not exist"


@dataclass(eq=False)
class UserNicknameNotExists(UserGatewayError):
    nickname: str

    @property
    def title(self) -> str:
        return f"A user with nickname `{self.nickname}` does not exist"
