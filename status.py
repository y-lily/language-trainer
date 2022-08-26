from __future__ import annotations

from enum import Enum


class Status(Enum):
    available = 1
    completed = 2
    delayed = 3

    def convert(obj: str | Status) -> Status:
        try:
            match obj.strip().lower():
                case Status.completed.name:
                    return Status.completed
                case Status.delayed.name:
                    return Status.delayed
        except AttributeError:
            pass

        match obj:
            case Status.completed:
                return Status.completed
            case Status.delayed:
                return Status.delayed

        return Status.available


if __name__ == "__main__":
    def custom_enum_test():
        print(Status.available)
        print(type(Status.available))
        print(Status.available.name)
        print(type(Status.available.name))

    def custom_convert_test():
        x = Status.completed
        print(Status.convert(x))
        y = "completed"
        print(Status.convert(y))

    # custom_enum_test()
    # custom_convert_test()
