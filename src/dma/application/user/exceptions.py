from dataclasses import dataclass

from dma.application.common.exceptions import DatabaseGatewayError


class UserDatabaseGatewayError(DatabaseGatewayError):
    pass


@dataclass(eq=False)
class UserIdNotExists(UserDatabaseGatewayError):  # noqa: N818
    id: int

    @property
    def title(self) -> str:
        return f"A user with id {self.id} does not exist"


@dataclass(eq=False)
class UserNicknameNotExists(UserDatabaseGatewayError):  # noqa: N818
    nickname: str

    @property
    def title(self) -> str:
        return f"A user with nickname `{self.nickname}` does not exist"
