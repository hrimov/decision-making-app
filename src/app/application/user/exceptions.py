from dataclasses import dataclass

from src.app.application.common.exceptions import DatabaseGatewayError


class UserDatabaseGatewayError(DatabaseGatewayError):
    pass


@dataclass(eq=False)
class UserIdNotExists(UserDatabaseGatewayError):
    id: int

    @property
    def title(self) -> str:
        return f"A user with id {self.id} does not exist"


@dataclass(eq=False)
class UserNicknameNotExists(UserDatabaseGatewayError):
    nickname: str

    @property
    def title(self) -> str:
        return f"A user with nickname `{self.nickname}` does not exist"
