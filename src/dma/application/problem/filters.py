from dataclasses import dataclass

from dma.application.common.filters import Filters


@dataclass(frozen=True)
class ProblemFilters(Filters):
    ...


@dataclass(frozen=True)
class ProblemStateFilters(Filters):
    ...
