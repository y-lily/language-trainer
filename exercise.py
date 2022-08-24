from __future__ import annotations


class Exercise:

    def __init__(self, task: str, body: str, solution: str = "",
                 status: str = "", difficulty: str = "",
                 tags: list[str] = []) -> None:
        self.__task = task
        self.__body = body
        self.__solution = solution
        self.__status = status
        self.__difficulty = difficulty
        self.__tags = tags

    def __str__(self) -> str:
        return (f"{self.__task} (*{self.__difficulty}): '{self.__body}'")

    def matches(self, task: str = "", body: str = "", status: str = "",
                difficulty: str = "", tags: list[str] = []) -> bool:
        """Check if the exercise satisfies all given restrictions."""
        return all([
            task in self.__task,
            body in self.__body,
            status in self.__status,
            difficulty in self.__difficulty,
            all(tag in self.__tags for tag in tags)
        ])

    def to_dump(self) -> object:
        return {"task": self.__task, "body": self.__body, "solution": self.__solution,
                "status": self.__status, "difficulty": self.__difficulty, "tags": self.__tags}

    def from_load(loaded: dict) -> Exercise:
        try:
            return Exercise(task=loaded["task"],
                            body=loaded["body"],
                            solution=loaded.get("solution", ""),
                            status=loaded.get("status", ""),
                            difficulty=loaded.get("difficulty", ""),
                            tags=loaded.get("tags", []))
        except KeyError:
            raise ValueError("Cannot convert from dict to Exercise. \
                At least one of 'task' and 'body' keys is missing.")

    # def __hash__(self) -> int:
    #     pass

    # def __eq__(self, __o: object) -> bool:
    #     pass

    # def check_solution(self, solution: str):
    #     """Tell if the suggested solution is correct, suboptimal or wrong."""
    #     pass


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

    def get_exercise() -> Exercise:
        task = input("Exercise task: ")
        body = input("Exercise body: ")
        solution = input("Solution to the exercise: ")
        status = input("Status of the exercise: ")
        difficulty = input("Difficulty of the exercise: ")

        tags = input("Tags separated by commas: ").split(",")
        tags = [tag.strip().lower() for tag in tags]

        return Exercise(task=task, body=body, solution=solution,
                        status=status, difficulty=difficulty, tags=tags)

    def dump_load_test():
        ex = get_exercise()
        print()
        print(ex)
        print()
        d = ex.to_dump()
        print(d)
        print()
        ex2 = Exercise.from_load(d)
        print(ex2)
        print()

    # run_test(str_test)
    # run_test(dump_load_test)
