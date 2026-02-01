from dataclasses import dataclass
from datetime import date
from typing import Literal


@dataclass(frozen=True)
class PeriodParseResult:
    from_date: date
    to_date: date
    granularity: Literal["day", "month", "range"]
    label: str
