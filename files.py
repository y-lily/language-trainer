import json
import platform


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
