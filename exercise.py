from __future__ import annotations

from status import Status


class Exercise:

    def __init__(self, task: str, body: str, solution: str = "",
                 status: str | Status = "", difficulty: str = "",
                 tags: list[str] = []) -> None:
        self.__task = task
        self.__body = body
        self.__solution = solution
        self.__status = Status.convert(status)
        self.__difficulty = difficulty
        self.__tags = tags

    def __eq__(self, other: object) -> bool:
        if type(self) is type(other):
            return all([self.__task == other.__task,
                        self.__body == other.__body,
                        self.__difficulty == other.__difficulty])
        return False

    def __hash__(self) -> int:
        return hash((self.__task, self.__body, self.__difficulty))

    def __str__(self) -> str:
        return (f"{self.__task} (*{self.__difficulty}): '{self.__body}'")

    def matches(self, task: str = "", body: str = "",
                solution: str = "", status: str | Status = "",
                difficulty: str = "", tags: list[str] = []) -> bool:
        """Check if the exercise satisfies all given restrictions."""
        return all([
            task in self.__task,
            body in self.__body,
            solution in self.__solution,
            not status or Status.convert(status) == self.__status,
            not difficulty or difficulty == self.__difficulty,
            all(tag in self.__tags for tag in tags)
        ])

    def to_dump(self) -> object:
        return {"task": self.__task, "body": self.__body, "solution": self.__solution,
                "status": self.__status.name, "difficulty": self.__difficulty, "tags": self.__tags}

    # def to_exercise(exercise_data: dict) -> Exercise:
    #     try:
    #         return Exercise(task=exercise_data["task"],
    #                         body=exercise_data["body"],
    #                         solution=exercise_data.get("solution", ""),
    #                         status=exercise_data.get("status", ""),
    #                         difficulty=exercise_data.get("difficulty", ""),
    #                         tags=exercise_data.get("tags", []))
    #     except KeyError:
    #         raise ValueError("Cannot convert from dict to Exercise. \
    #             At least one of 'task' and 'body' keys is missing.")

    def make_available(self) -> None:
        self.__status = Status.available

    def make_completed(self) -> None:
        self.__status = Status.completed

    def make_delayed(self) -> None:
        self.__status = Status.delayed

    def is_available(self) -> bool:
        return self.__status == Status.available

    def refresh(self) -> None:
        if self.__status == Status.delayed:
            self.make_available()

    def replace(self, new_: Exercise) -> None:
        self.__task = new_.__task
        self.__body = new_.__body
        self.__solution = new_.__solution
        self.__status = new_.__status
        self.__difficulty = new_.__difficulty
        self.__tags = new_.__tags

    @property
    def solution(self) -> str:
        return self.__solution

    # @property
    # def status(self) -> Status:
    #     return self.__status
