from functools import partial
import json
import platform
import shutil


def run_ui() -> None:
    lang1 = input("The language you are practicing: ")
    lang2 = input(
        "Your native language (or the one you want to use as the secondary): ")

    exercises_fn = make_fn(lang1, lang2, "exerc")
    exercises = load(exercises_fn, [])

    while True:
        print(f"{filled_line()}\n"
              f"{filled_line('   MAIN MENU   ')}\n"
              f"{filled_line()}\n"
              f"Do you want to: \n"
              f"  (v)iew exercises [{len(exercises)} total]\n"
              f"  (a)dd new exercises\n"
              f"  (q)uit\n")

        option = input("Option: ").strip().lower()

        if option in ("q", "quit", "exit"):
            break
        if option in ("v", "view", "view exercises"):
            repeat(partial(view, exercises),
                   "Look for another exercises? [Y/n] ")
        if option in ("a", "add", "add exercises", "add new exercises"):
            repeat(partial(add, exercises), "Add another exercise? [Y/n] ")

    if ask("Save changes? [Y/n] "):
        dump(exercises, exercises_fn)


def repeat(action: partial, repeat_question: str = "Repeat the action? [Y/n] "):
    while True:
        try:
            action()
        except EOFError:
            return

        if not ask(repeat_question):
            return


def add(exercises: list[dict]) -> None:
    print(f"{filled_line('   ADD EXERCISE   ')}")
    task = input("Exercise task: ")
    body = input("Exercise body: ")
    solution = input("Solution to the exercise: ")
    status = input("Status of the exercise: ")
    difficulty = input("Difficulty of the exercise: ")

    exercises.append({"task": task, "body": body, "solution": solution,
                      "status": status, "difficulty": difficulty})

    print("The exercise has been successfully added.")


def view(exercises: list[dict]) -> None:
    print(f"{filled_line('   VIEW EXERCISES   ')}")
    task = input("Task should contain: ")
    body = input("Body should contain: ")
    status = input("Status should contain: ")
    difficulty = input("Difficulty should contain: ")
    found = find(exercises=exercises, task=task, body=body,
                 status=status, difficulty=difficulty)

    print(f"{filled_line('   SEARCH RESULTS   ')}")
    if not found:
        print("No matches found.")
    for f in found:
        print(f)


def find(exercises: list[dict], task: str = "", body: str = "", status: str = "", difficulty: str = "") -> list[dict]:
    return [ex for ex in exercises if all([task in ex["task"],
                                          body in ex["body"],
                                          status in ex["status"],
                                          difficulty in ex["difficulty"]])]


def ask(prompt: str) -> bool:
    while True:
        answer = input(prompt).strip().lower()

        if answer in ("yes", "y", ""):
            return True
        if answer in ("no", "n"):
            return False


def make_fn(*args: str, sep: str = "-", ext: str = "json", fe: bool = False) -> str:
    fn = sep.join(str(a).lower() for a in args)
    if platform.system() == "Windows" or fe:
        fn += "." + ext.lstrip(".")
    return fn


def load(fn: str, default: object = None) -> object:
    try:
        with open(fn, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def dump(obj: object, fn: str) -> None:
    with open(fn, "w") as file:
        json.dump(obj, file, separators=(",\n", ": "))


def filled_line(txt: str = "", fil: str = "*") -> str:
    return f"{txt :{fil}^{shutil.get_terminal_size().columns}}"


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

    # run_test(ask_test)
    # run_test(make_fn_test)
    # run_test(filled_line_test)

    run_ui()
