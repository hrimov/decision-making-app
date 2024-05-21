import datetime

from abc import ABC


class DTO(ABC):  # noqa: B024
    pass


class StartedEndedAtMixin(DTO):
    started_at: datetime.datetime
    ended_at: datetime.datetime
