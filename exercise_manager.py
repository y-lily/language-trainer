from __future__ import annotations

from typing import Any, Iterator

from difficulty import Difficulty
from exercise import Exercise
from status import Status


class ExerciseManager:

    def __init__(self, exercises: list[Exercise] = None) -> None:
        self._exercises = exercises if exercises else []

    def __getitem__(self, _s: slice) -> ExerciseManager:
        return ExerciseManager(self._exercises.__getitem__(_s))

    def __iter__(self) -> Iterator[Exercise]:
        return self._exercises.__iter__()

    def __len__(self) -> int:
        return len(self._exercises)

    def __next__(self) -> Any:
        return self._exercises.__next__()

    def __str__(self) -> str:
        return "\n".join(f"{n}. {str(ex)}" for n, ex in enumerate(self._exercises))

    @classmethod
    def from_load(cls, loaded: list) -> ExerciseManager:
        return ExerciseManager([Exercise(**obj) for obj in loaded])

    def add(self, exercise: Exercise) -> None:
        self._exercises.append(exercise)

    def find(self, _task: str = "", _body: str = "",
             _solution: str = "", _status: str | Status = None,
             _difficulty: str | Difficulty = None, _tags: list[str] = None) -> ExerciseManager:

        found = [ex for ex in self._exercises if ex.matches(_task=_task,
                                                            _body=_body,
                                                            _solution=_solution,
                                                            _status=_status,
                                                            _difficulty=_difficulty,
                                                            _tags=_tags)]
        return ExerciseManager(found)

    def insert(self, index: int, exercise: Exercise) -> None:
        self._exercises.insert(index, exercise)

    def pop(self, index: int) -> None:
        self._exercises.pop(index)

    def refresh(self) -> None:
        for exercise in self._exercises:
            if exercise.is_delayed():
                exercise.make_available()

    def remove(self, exercise: Exercise) -> None:
        self._exercises.remove(exercise)

    def to_dump(self) -> list[dict[str, Any]]:
        return [ex.to_dump() for ex in self._exercises]

    def update(self, new_: Exercise) -> bool:
        """If the manager contains an equal exercise, replace it with the given one and return True, 
        which means there has been an actual update.

        Otherwise, add the given exercise to the manager and return False, which means the action 
        performed is no different from the method 'add'."""
        old = next((ex for ex in self._exercises if ex == new_), None)

        if not old:
            self.add(new_)
            return False

        old.update(new_)
        return True
