from __future__ import annotations
from functools import partial


from exercise import Exercise
from exercise_manager import ExerciseManager
from files import dump, load, make_fn
from interface import ask, ask_exercise_info, cls, filled_line


class ExerciseBuilder:
    def __init__(self, lang1: str, lang2: str) -> None:
        self.__exercises_fn = make_fn(lang1, lang2, "exerc")
        self.__exercises = ExerciseManager.to_exercise_manager(
            load(self.__exercises_fn, []))

    def __enter__(self) -> ExerciseBuilder:
        return self

    def __exit__(self, *_) -> None:
        if ask("Save changes? [Y/n] "):
            print("Saving...")
            self.__save_changes()

    def __save_changes(self) -> None:
        dump(self.__exercises.to_dump(), self.__exercises_fn)

    def run_ui(self):
        while True:
            cls()
            print(f"{filled_line()}\n"
                  f"{filled_line('   MAIN MENU   ')}\n"
                  f"{filled_line()}\n"
                  f"Do you want to: \n"
                  f"  (v)iew exercises [{len(self.__exercises)} total]\n"
                  f"  (a)dd new exercises\n"
                  f"  (q)uit\n")

            option = input("Option: ").strip().lower()

            if option in ("q", "quit", "exit"):
                return

            if option in ("v", "view", "view exercises"):
                repeat(self.view, "Look for another exercises? [Y/n] ")

            if option in ("a", "add", "add exercises", "add new exercises"):
                repeat(self.add,
                       "The exercise has been successfully added. Add another exercise? [Y/n] ")

    def add(self) -> None:
        info = ask_exercise_info(
            "Choose what you want to change or leave it empty to finish with editing.")
        self.__exercises.add(Exercise.to_exercise(info))

    def find(self) -> list[Exercise]:
        info = ask_exercise_info(
            "Choose filters or leave them empty to view all exercises.\n")

        return self.__exercises.find(**info)

    def view(self) -> None:
        found = self.find()

        print(f"{filled_line('   SEARCH RESULTS   ')}")
        if not found:
            print("No matches found.")
        for f in found:
            print(f)


def repeat(action: partial, repeat_question: str = "Repeat the action? [Y/n] "):
    while True:
        try:
            action()
        except EOFError:
            return

        if not ask(repeat_question):
            return


if __name__ == "__main__":

    def run_test(test):
        print(f"\nTesting {test}.")
        while True:
            try:
                test()
            except (EOFError):
                break
        print("\nThe test is over.")

    def ask_test():
        if ask("Yes or no? [Y/n] "):
            print("You answered yes.")
        else:
            print("You answered no.")

    def make_fn_test():
        print("Exercise manager name for your system: ")
        print(make_fn("fi", "en", "exerc"))
        arg1, arg2 = input("Two args separated by a comma: ").split(",")
        sep = input("sep: ")
        ext = input("ext: ")
        fe = ask("fe on? [Y/n] ")
        print(make_fn(arg1, arg2, sep=sep, ext=ext, fe=fe))

    def filled_line_test():
        txt = input("Text: ")
        print(filled_line(txt))

    def ask_exercise_info_test():
        d = ask_exercise_info("Edit the options: ")
        print()
        print(d)
        print()
        print(Exercise.to_exercise(d))

    # run_test(ask_test)
    # run_test(make_fn_test)
    # run_test(filled_line_test)
    # run_test(ask_exercise_info_test)

    with ExerciseBuilder("fi", "en") as eb:
        eb.run_ui()
