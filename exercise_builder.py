from __future__ import annotations
from functools import partial

import json
import os
import platform
import shutil

from exercise_manager import ExerciseManager
from exercise import Exercise


class ExerciseBuilder:
    def __init__(self, lang1: str, lang2: str) -> None:
        self.__exercises_fn = make_fn(lang1, lang2, "exerc")
        self.__exercises = ExerciseManager.from_load(
            load(self.__exercises_fn, []))

    def __enter__(self) -> ExerciseBuilder:
        return self

    def __exit__(self, *_) -> None:
        if ask("Save changes? [Y/n] "):
            print("Saving...")
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
                break

            if option in ("v", "view", "view exercises"):
                repeat(self.view, "Look for another exercises? [Y/n] ")

            if option in ("a", "add", "add exercises", "add new exercises"):
                repeat(self.add,
                       "The exercise has been successfully added. Add another exercise? [Y/n] ")

    def add(self) -> None:
        info = ask_exercise_info(
            "Choose what you want to change or leave it empty to finish with editing.")
        self.__exercises.add(Exercise.from_load(info))

    def view(self) -> None:
        info = ask_exercise_info(
            "Choose filters or leave them empty to view all exercises.\n")

        found = self.__exercises.find(task=info["task"],
                                      body=info["body"],
                                      status=info["status"],
                                      difficulty=info["difficulty"],
                                      tags=info["tags"])

        print(f"{filled_line('   SEARCH RESULTS   ')}")
        if not found:
            print("No matches found.")
        for f in found:
            print(f)


def make_fn(*args: str, sep: str = "-", ext: str = "json", fe: bool = False) -> str:
    fn = sep.join(str(a).lower() for a in args)
    if platform.system() == "Windows" or fe:
        fn += "." + ext.lstrip(".")
    return fn


def cls() -> None:
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def filled_line(txt: str = "", fil: str = "*") -> str:
    return f"{txt :{fil}^{shutil.get_terminal_size().columns}}"


def repeat(action: partial, repeat_question: str = "Repeat the action? [Y/n] "):
    while True:
        try:
            action()
        except EOFError:
            return

        if not ask(repeat_question):
            return


def ask(prompt: str) -> bool:
    while True:
        answer = input(prompt).strip().lower()

        if answer in ("yes", "y", ""):
            return True
        if answer in ("no", "n"):
            return False


def ask_exercise_info(prompt: str) -> dict:
    blank = Exercise(task="", body="").to_dump()
    info = {str(n): [k, v] for n, (k, v) in enumerate(blank.items())}

    while True:
        cls()
        print(f"{filled_line()}\n"
              f"{filled_line('   EDIT INFO   ')}\n"
              f"{filled_line()}\n"
              f"{prompt}\n")
        print("\n".join(f"{n} ({k}): {v}" for n, (k, v) in info.items()))

        variable = input(
            "Variable ('q' or empty line to stop): ").strip().lower()
        if variable in ("q", "quit", "exit", ""):
            info = {k: v for _, (k, v) in info.items()}
            try:
                info["tags"] = [tag.strip() for tag in info["tags"].split(",")]
            except AttributeError:
                pass
            return info
        if variable in info.keys():
            info[variable][1] = input(f"Edit {info[variable][0]}: ")


def load(fn: str, default: object = None) -> object:
    try:
        with open(fn, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def dump(obj: object, fn: str) -> None:
    with open(fn, "w") as file:
        json.dump(obj, file, separators=(",\n", ": "))


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
        print(Exercise.from_load(d))

    # run_test(ask_test)
    # run_test(make_fn_test)
    # run_test(filled_line_test)
    # run_test(ask_exercise_info_test)

    with ExerciseBuilder("fi", "en") as eb:
        eb.run_ui()
