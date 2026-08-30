from datetime import date
from typing import NamedTuple


class _SkipPeriod(NamedTuple):
    start: date
    end: date
    reason: str


SKIP_PERIODS = [
    _SkipPeriod(start=date(2023, 3, 23), end=date(2023, 4, 3), reason="Move"),
    _SkipPeriod(start=date(2023, 5, 31), end=date(2023, 6, 2), reason="Move"),
    _SkipPeriod(start=date(2024, 5, 24), end=date(2024, 6, 3), reason="Move"),
    _SkipPeriod(start=date(2025, 4, 28), end=date(2025, 5, 1), reason="Move"),
    _SkipPeriod(start=date(2026, 8, 19), end=date(2026, 8, 22), reason="Sensor issue"),
]
