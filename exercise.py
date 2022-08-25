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

    def matches(self, task: str = "", body: str = "", status: str | Status = "",
                difficulty: str = "", tags: list[str] = []) -> bool:
        """Check if the exercise satisfies all given restrictions."""
        return all([
            task in self.__task,
            body in self.__body,
            not status or Status.convert(status) == self.__status,
            not difficulty or difficulty == self.__difficulty,
            all(tag in self.__tags for tag in tags)
        ])

    def to_dump(self) -> object:
        return {"task": self.__task, "body": self.__body, "solution": self.__solution,
                "status": self.__status.name, "difficulty": self.__difficulty, "tags": self.__tags}

    def to_exercise(exercise_data: dict) -> Exercise:
        try:
            return Exercise(task=exercise_data["task"],
                            body=exercise_data["body"],
                            solution=exercise_data.get("solution", ""),
                            status=exercise_data.get("status", ""),
                            difficulty=exercise_data.get("difficulty", ""),
                            tags=exercise_data.get("tags", []))
        except KeyError:
            raise ValueError("Cannot convert from dict to Exercise. \
                At least one of 'task' and 'body' keys is missing.")

    def complete(self) -> None:
        self.__status = Status.completed

    @property
    def solution(self) -> str:
        return self.__solution

    @property
    def status(self) -> Status:
        return self.__status


if __name__ == "__main__":
    def run_test(test):
        print(f"\nTesting {test}.")
        while True:
            try:
                test()
            except (EOFError):
                break
        print("\nThe test is over.")

    def str_test():
        task = input("Task: ")
        body = input("Body: ")
        difficulty = input("Difficulty: ")
        print(Exercise(task=task, body=body, difficulty=difficulty))

    from exercise_builder import ask, ask_exercise_info

    def dump_load_test():
        info = ask_exercise_info("Edit your exercise here.")
        print()
        print(info)
        print()

        ex = Exercise.to_exercise(info)
        print(ex)
        print()

        print(ex.to_dump())
        print()
        if not ask("Repeat? [Y/n] "):
            raise EOFError

    def eq_test():
        ex1 = Exercise.to_exercise(
            ask_exercise_info("Edit the first exercise."))
        while True:
            ex2 = Exercise.to_exercise(
                ask_exercise_info("Edit the second exercise. Equal exercises should have equal tasks, bodies and difficulties.", ex1))

            print(f"{ex1}\n"
                  f"{ex2}\n"
                  f"ex1 {'is' if ex1 == ex2 else 'is not'} equal to ex2")

            if not ask("Repeat? [Y/n] "):
                raise EOFError

    # run_test(str_test)
    # run_test(dump_load_test)
    # run_test(eq_test)
