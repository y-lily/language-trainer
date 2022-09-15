from __future__ import annotations

from enum import Enum


class Status(Enum):
    available = 1
    completed = 2
    delayed = 3

    def convert(obj: str | Status) -> Status:
        try:
            return Status[obj.strip().lower()]
        except (AttributeError, KeyError):
            return obj if obj in Status.__members__.values() else Status.available
