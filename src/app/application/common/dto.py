import datetime

from abc import ABC


class DTO(ABC):
    pass


class StartedEndedAtMixin(DTO):
    started_at: datetime.datetime
    ended_at: datetime.datetime
