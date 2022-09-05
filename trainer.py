from __future__ import annotations

from exercise import Exercise
from exercise_manager import ExerciseManager
from files import dump, load, make_fn
from interface import ask, ask_exercise_info, clean, cls, filled_line


class Trainer:
    def __init__(self, lang1: str, lang2: str) -> None:
        self.__exercises_fn = make_fn(lang1, lang2, "exerc")
        self.__exercises = ExerciseManager.to_exercise_manager(
            load(self.__exercises_fn, []))

        self.__lesson_fn = Trainer.__current_lesson_fn(lang1, lang2)
        self.__lesson = ExerciseManager.to_exercise_manager(
            load(self.__lesson_fn, []))

    def __enter__(self) -> Trainer:
        return self

    def __exit__(self, *_) -> None:
        if ask("Save changes? [Y/n] "):
            print("Saving...")
            self.__save_changes()

    def __save_changes(self) -> None:
        self.refresh()
        for exercise in self.__lesson:
            self.__exercises.update(exercise)

        self.__lesson = ExerciseManager(
            [ex for ex in self.__lesson if ex.is_available()])

        dump(self.__exercises.to_dump(), self.__exercises_fn)
        dump(self.__lesson.to_dump(), self.__lesson_fn)

    def __current_lesson_fn(lang1: str, lang2: str) -> str:
        # TODO: Make it pick the last file.
        return make_fn(lang1, lang2, "lesson")

    def find(self) -> list[Exercise]:
        info = ask_exercise_info(
            "Choose filters or leave them empty to view all exercises.\n")

        return self.__exercises.find(**info)

    def run_ui(self):
        while True:
            cls()
            exercise = self.next_available()
            if not exercise:
                print("No available exercises left.")
                if ask("View skipped exercises? [Y/n] "):
                    self.refresh()
                    exercise = self.next_available()

            if not exercise:
                print("Nothing to train. You can look for new exercises or quit.")
                exercise = Exercise(task="", body="")

            print(f"{filled_line()}\n"
                  f"{filled_line('   THE TRAINER   ')}\n"
                  f"{filled_line()}\n"
                  f"Do you want to: \n"
                  f"  (a)nswer\n"
                  f"  (s)kip\n"
                  f"  (f)ind similar exercises\n"
                  f"  (c)reate a new exercise\n"
                  f"  (q)uit\n"
                  f"{exercise}\n")

            option = input("Option: ").strip().lower()

            if option in ("q", "quit", "exit"):
                break

            if option in ("a", "answer"):
                self.solve(exercise, input("Your solution: "))

            if option in ("s", "skip"):
                exercise.make_delayed()

            if option in ("f", "find", "find similar"):
                curr_ex_index = self.next_available_index()

                for ex in self.find():
                    if ex not in self.__lesson:
                        self.__lesson.insert(curr_ex_index, ex)

            if option in ("c", "create"):
                new_ = Exercise(**ask_exercise_info(
                    "Edit the exercise you want to add.", exercise))
                self.__lesson.add(new_)

    # def add(self, exercise: Exercise) -> None:
    #     self.__lesson.add(exercise)

    # TODO: Treat slightly incorrect solutions as correct and potentially
    # working solutions as suboptimal.
    # Ways to achieve this:
    # a). Save a dictionary with words and phrases. When a given solution does
    # not match the required solution, the dictionary should be addressed.
    # b). Save the solution as a group of replaceable parts.
    def solve(self, exercise: Exercise, solution: str):
        # if not clean(solution) == clean(exercise.solution):
        #     check(self.__dictionary)
        if clean(solution) == clean(exercise.solution):
            exercise.make_completed()
        if ask("View the solution? [Y/n] "):
            print(exercise.solution)
        if ask("Mark as completed? [Y/n] "):
            exercise.make_completed()

    def refresh(self) -> None:
        self.__lesson.refresh()

    def next_available(self) -> Exercise:
        return next((ex for ex in self.__lesson if ex.is_available()), None)

    def next_available_index(self) -> int:
        return next((n for n, ex in enumerate(self.__lesson) if ex.is_available()), 0)


if __name__ == "__main__":
    with Trainer("fi", "en") as tr:
        tr.run_ui()
