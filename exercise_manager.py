from __future__ import annotations

from exercise import Exercise


class ExerciseManager:

    def __init__(self, exercises: list[Exercise] = []) -> None:
        self.__exercises = exercises

    def __len__(self) -> int:
        return len(self.__exercises)

    def __iter__(self):
        return self.__exercises.__iter__()

    def __next__(self):
        return self.__exercises.__next__()

    def add(self, exercise: Exercise) -> None:
        self.__exercises.append(exercise)

    def find(self, task: str = "", body: str = "", status: str = "",
             difficulty: str = "", tags: list[str] = []) -> list[Exercise]:
        return [ex for ex in self.__exercises if ex.matches(task=task,
                                                            body=body,
                                                            status=status,
                                                            difficulty=difficulty,
                                                            tags=tags)]

    def to_dump(self) -> object:
        return [ex.to_dump() for ex in self.__exercises]

    def to_exercise_manager(loaded: list) -> ExerciseManager:
        return ExerciseManager([Exercise.to_exercise(obj) for obj in loaded])


if __name__ == "__main__":
    def run_test(test):
        print(f"\nTesting {test}.")
        while True:
            try:
                test()
            except (EOFError):
                break
        print("\nThe test is over.")

    from exercise_builder import ask, ask_exercise_info

    def iteration_test():
        manager = ExerciseManager()

        while True:
            try:
                info = ask_exercise_info("")
                manager.add(Exercise.to_exercise(info))
            except EOFError:
                break

        print()
        for x in manager:
            print(x)

        if not ask("Repeat test? [Y/n] "):
            raise EOFError

    def custom_iteration_test():
        manager = ExerciseManager()
        manager.add(Exercise(task="Write this in English.",
                             body="Väinö, onko sinulla suomalainen nimi?",
                             solution="Väinö, do you have a Finnish name?",
                             difficulty="easy"))

        manager.add(Exercise(task="Write this in Finnish.",
                             body="Liisa, do you have a Norwegian cat?",
                             solution="Liisa, onko sinulla norjalainen kissa?",
                             difficulty="medium"))

        print("Should print: ")
        print("Write this in English. (*easy): 'Väinö, onko sinulla suomalainen nimi?'\n"
              "Write this in Finnish. (*medium): 'Liisa, do you have a Norwegian cat?'")
        print("Prints: ")
        for ex in manager:
            print(ex)

    # run_test(iteration_test)
    # custom_iteration_test()
