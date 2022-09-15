from __future__ import annotations

from exercise_manager import ExerciseManager
from interface import ask
from files import dump, load, make_fn


class BaseUI:
    _ADD_PROMPT = ("Type in the indices of the exercises you want to add separated by commas.\n"
                   "You can specify ranges: the query '1, 3-5' will add the exercises 1, 3, 4, 5.")

    _EDIT_PROMPT = "You can edit the exercise info here. Leave the input empty to exit the editing."

    _REMOVE_PROMPT = ("Type in the indices of the exercises you want to remove separated by commas.\n"
                      "You can specify ranges: the query '1, 3-5' will remove the exercises 1, 3, 4, 5.")

    def __init__(self, lang1: str, lang2: str) -> None:
        self._exercise_pool_fn = make_fn(lang1, lang2, "exerc")
        self._exercise_pool = ExerciseManager.from_load(
            load(self._exercise_pool_fn, []))

        self._new_exercises_fn = make_fn(lang1, lang2, "new", "exerc")
        self._new_exercises = ExerciseManager.from_load(
            load(self._new_exercises_fn, []))

    def __enter__(self) -> BaseUI:
        return self

    def __exit__(self, *_) -> None:
        if ask("Save changes?"):
            print("Saving...")
            self._save_changes()

    def _save_changes(self) -> None:
        dump(self._exercise_pool.to_dump(), self._exercise_pool_fn)
        dump(self._new_exercises.to_dump(), self._new_exercises_fn)

    def build_menu_prompt(self) -> str:
        pass

    def run_ui(self) -> None:
        pass
