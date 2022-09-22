from __future__ import annotations

import copy
from typing import Any

from difficulty import Difficulty
from status import Status


class Exercise:

    def __init__(self, _task: str, _body: str,
                 _solution: str = "", _status: str | Status = None,
                 _difficulty: str | Difficulty = None, _tags: list[str] = None) -> None:
        self._task = _task
        self._body = _body
        self._solution = _solution
        self._status = Status.convert(_status)
        self._difficulty = Difficulty.convert(_difficulty)
        self._tags = _tags if _tags else []

    def __eq__(self, other: object) -> bool:
        if type(self) is type(other):
            return all([self._task == other._task,
                        self._body == other._body,
                        self._difficulty is other._difficulty])

        return False

    def __hash__(self) -> int:
        return hash((self._task, self._body, self._difficulty))

    def __str__(self) -> str:
        return (f"{self._task} (*{self._difficulty.name}): '{self._body}'")

    @property
    def solution(self) -> str:
        return self._solution

    def is_available(self) -> bool:
        return self._status is Status.available

    def is_completed(self) -> bool:
        return self._status is Status.completed

    def is_delayed(self) -> bool:
        return self._status is Status.delayed

    def make_available(self) -> None:
        self._status = Status.available

    def make_completed(self) -> None:
        self._status = Status.completed

    def make_delayed(self) -> None:
        self._status = Status.delayed

    def matches(self, _task: str = "", _body: str = "",
                _solution: str = "", _status: str | Status = None,
                _difficulty: str | Difficulty = None, _tags: list[str] = None) -> bool:
        """Check if the exercise satisfies all given restrictions."""
        return all([
            _task in self._task,
            _body in self._body,
            _solution in self._solution,
            not _status or Status.convert(_status) is self._status,
            not _difficulty or Difficulty.convert(
                _difficulty) is self._difficulty,
            not _tags or all(tag in self._tags for tag in _tags)
        ])

    def to_dump(self) -> dict[str, Any]:
        dumpable = copy.deepcopy(vars(self))

        dumpable["_status"] = self._status.name
        dumpable["_difficulty"] = self._difficulty.name

        return dumpable

    def update(self, new_: Exercise) -> None:
        vars(self).update(vars(new_))
