from functools import partial
import os
import platform
import shutil

from exercise import Exercise
from exercise_manager import ExerciseManager


def ask(prompt: str) -> bool:
    if not prompt.rstrip().endswith("[Y/n]"):
        prompt += " [Y/n] "

    while True:
        answer = input(prompt).strip().lower()

        if answer in ("yes", "y", ""):
            return True
        if answer in ("no", "n"):
            return False


def ask_exercise_info(prompt: str, base_exercise: Exercise = None) -> dict:
    # Note to future myself: here, I learned it the hard way that you should NOT use mutable objects as default arguments.
    if not base_exercise:
        base_exercise = Exercise(_task="", _body="")

    info = {str(n): [k, v]
            for n, (k, v) in enumerate(base_exercise.to_dump().items())}

    while True:
        print(f"{filled_line()}\n"
              f"{prompt}\n"
              f"{filled_line()}\n")

        print("\n".join(f"{n}. ({clean(k)}): {v}" for n,
              (k, v) in info.items()))

        user_input = input(
            "Variable ('q' or empty line to stop): ").strip().lower()

        if user_input in ("q", "quit", "exit", ""):
            info = {k: v for _, (k, v) in info.items()}
            try:
                info["_tags"] = [tag.strip()
                                 for tag in info["_tags"].split(",") if tag.strip()]
            except AttributeError:
                pass
            return info

        if user_input in info.keys():
            info[user_input][1] = input(f"Edit {clean(info[user_input][0])}: ")


def clean(string_: str) -> str:
    return "".join(s.lower() for s in string_ if s.isalnum())


def clearscreen() -> None:
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def filled_line(txt: str = "", fil: str = "*") -> str:
    return f"{txt :{fil}^{shutil.get_terminal_size().columns}}"


def parse_ranges(ranges: str) -> list[int]:
    result = []

    parts = ranges.split(",")

    for part in parts:
        if "-" in part:
            (start, end) = sorted([int(clean(p)) for p in part.split("-")])
            result.extend(range(start, end + 1))
        else:
            result.append(int(clean(part)))

    return result


def print_search_results(found: ExerciseManager) -> None:
    print(f"{filled_line('   SEARCH RESULTS   ')}")
    if not found:
        print("No matches found.")
    print(found)


def repeat(action: partial, repeat_question: str = "Repeat the action? [Y/n] "):
    while True:
        try:
            action()
        except EOFError:
            return

        if not ask(repeat_question):
            return
