from __future__ import annotations


from exercise import Exercise
from exercise_manager import ExerciseManager
from files import dump, load, make_fn
from interface import ask, ask_exercise_info, cls, filled_line, parse_ranges, repeat


class ExerciseBuilder:
    __EDIT_PROMPT = "You can edit the new exercise here. Leave the input empty to exit the editing."

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

    def add(self) -> None:
        info = ask_exercise_info(self.__EDIT_PROMPT)
        self.__exercises.add(Exercise(**info))

    def find(self) -> list[Exercise]:
        info = ask_exercise_info(self.__EDIT_PROMPT)
        return self.__exercises.find(**info)

    def remove(self) -> None:
        found = self.find()
        ExerciseBuilder.print_search_results(found)

        print("Type in the indices you want to remove, separated by commas.\n"
              "You can specify ranges with '-'. For instance, the query '1, 3-5, 7' will remove the exercises with indices 1, 3, 4, 5, 7.")

        for index in parse_ranges(input()):
            try:
                self.__exercises.remove(found[index])
            except IndexError:
                print(
                    f"Failed to remove the item #{index}: there is no such index.")

    def run_ui(self):
        while True:
            cls()
            print(f"{filled_line()}\n"
                  f"{filled_line('   MAIN MENU   ')}\n"
                  f"{filled_line()}\n"
                  f"Do you want to: \n"
                  f"  (v)iew exercises [{len(self.__exercises)} total]\n"
                  f"  (a)dd new exercises\n"
                  f"  (r)emove existing exercises\n"
                  f"  (q)uit\n")

            option = input("Option: ").strip().lower()

            if option in ("q", "quit", "exit"):
                return

            if option in ("v", "view", "view exercises"):
                repeat(self.view, "Look for another exercises? [Y/n] ")

            if option in ("a", "add", "add exercises", "add new exercises"):
                repeat(self.add,
                       "The exercise has been successfully added. Add another exercise? [Y/n] ")

            if option in ("r", "rm", "remove", "remove exercises", "remove existing exercises"):
                repeat(
                    self.remove, "The removal has been completed. Remove another exercises? [Y/n] ")

    def view(self) -> None:
        ExerciseBuilder.print_search_results(self.find())

    def print_search_results(found) -> None:
        print(f"{filled_line('   SEARCH RESULTS   ')}")
        if not found:
            print("No matches found.")
        for n, f in enumerate(found):
            print(f"{n}: {f}")


if __name__ == "__main__":
    with ExerciseBuilder("fi", "en") as eb:
        eb.run_ui()
