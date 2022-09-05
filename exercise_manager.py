from __future__ import annotations

from exercise import Exercise


class ExerciseManager:

    def __init__(self, exercises: list[Exercise] = []) -> None:
        self._exercises = exercises

    def __getitem__(self, slice):
        return self._exercises.__getitem__(slice)

    def __iter__(self):
        return self._exercises.__iter__()

    def __len__(self) -> int:
        return len(self._exercises)

    def __next__(self):
        return self._exercises.__next__()

    def add(self, exercise: Exercise) -> None:
        self._exercises.append(exercise)

    def find(self, task: str = "", body: str = "", solution="", status: str = "",
             difficulty: str = "", tags: list[str] = []) -> list[Exercise]:
        return [ex for ex in self._exercises if ex.matches(task=task,
                                                           body=body,
                                                           solution=solution,
                                                           status=status,
                                                           difficulty=difficulty,
                                                           tags=tags)]

    def insert(self, index: int, exercise: Exercise) -> None:
        self._exercises.insert(index, exercise)

    def pop(self, index: int) -> None:
        self._exercises.pop(index)

    def refresh(self) -> None:
        for exercise in self._exercises:
            exercise.refresh()

    def remove(self, exercise: Exercise) -> None:
        self._exercises.remove(exercise)

    def to_dump(self) -> object:
        return [ex.to_dump() for ex in self._exercises]

    def to_exercise_manager(loaded: list) -> ExerciseManager:
        return ExerciseManager([Exercise(**obj) for obj in loaded])

    def update(self, new_: Exercise) -> None:
        """If the manager contains an equal exercise, such exercise is replaced with the given one.
        Otherwise, add the given exercise to the manager."""
        old = next((ex for ex in self._exercises if ex == new_), None)
        if not old:
            self.add(new_)
        else:
            old.replace(new_)
