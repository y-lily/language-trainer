from __future__ import annotations

from enum import Enum


class Status(Enum):
    available = 1
    completed = 2
    delayed = 3

    def convert(obj: str | Status) -> Status:
        try:
            match obj.strip().lower():
                case Status.completed.name:
                    return Status.completed
                case Status.delayed.name:
                    return Status.delayed
        except AttributeError:
            pass

        match obj:
            case Status.completed:
                return Status.completed
            case Status.delayed:
                return Status.delayed

        return Status.available
