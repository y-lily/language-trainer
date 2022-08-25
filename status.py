from __future__ import annotations

from enum import Enum


class Status(Enum):
    available = 1
    completed = 2

    def convert(obj: object) -> Status:
        try:
            if obj.strip().lower() == Status.completed.name:
                return Status.completed
        except AttributeError:
            pass

        if obj == Status.completed:
            return Status.completed

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
