from dataclasses import dataclass

from src.app.application.common.filters import Filters


@dataclass(frozen=True)
class ProblemFilters(Filters):
    ...


@dataclass(frozen=True)
class ProblemStateFilters(Filters):
    ...
