from __future__ import annotations

from enum import Enum


class Difficulty(Enum):
    easy = 1
    medium = 2
    hard = 3

    def convert(obj: str | Difficulty) -> Difficulty:
        try:
            return Difficulty[obj.strip().lower()]
        except (AttributeError, KeyError):
            return obj if obj in Difficulty.__members__.values() else Difficulty.easy
