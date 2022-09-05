from functools import partial
import os
import platform
import shutil

from exercise import Exercise


def ask(prompt: str) -> bool:
    while True:
        answer = input(prompt).strip().lower()

        if answer in ("yes", "y", ""):
            return True
        if answer in ("no", "n"):
            return False


def ask_exercise_info(prompt: str, base: Exercise = Exercise(task="", body="")) -> dict:
    info = {str(n): [k, v] for n, (k, v) in enumerate(base.to_dump().items())}

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


def clean(string_: str) -> str:
    return "".join(s.lower() for s in string_ if s.isalnum())


def cls() -> None:
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


def repeat(action: partial, repeat_question: str = "Repeat the action? [Y/n] "):
    while True:
        try:
            action()
        except EOFError:
            return

        if not ask(repeat_question):
            return
