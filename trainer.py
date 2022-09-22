from __future__ import annotations

from base_ui import BaseUI
from exercise import Exercise
from exercise_manager import ExerciseManager
from files import dump, load, make_fn
from interface import ask, ask_exercise_info, clean, filled_line, parse_ranges, print_search_results
from status import Status


class Trainer(BaseUI):
    def __init__(self, lang1: str, lang2: str) -> None:
        super().__init__(lang1, lang2)

        self._lesson_fn = Trainer._current_lesson_fn(lang1, lang2)
        self._lesson = ExerciseManager.from_load(
            load(self._lesson_fn, []))

        self._show_available_on = False

    def _current_lesson_fn(lang1: str, lang2: str) -> str:
        # TODO: Make it pick the last file.
        return make_fn(lang1, lang2, "lesson")

    def _save_changes(self) -> None:
        self.refresh()

        for exercise in self._lesson:
            if not self._exercise_pool.update(exercise):
                self._new_exercises.add(exercise)

        self._lesson = ExerciseManager(
            [ex for ex in self._lesson if ex.is_available()])

        dump(self._lesson.to_dump(), self._lesson_fn)
        super()._save_changes()

    def available(self) -> ExerciseManager:
        return self._lesson.find(_status=Status.available)

    def build_menu_prompt(self) -> str:
        exercise = self.next_available()

        prompt = f"{filled_line()}\n"
        prompt += f"{filled_line('   THE TRAINER   ')}\n"
        prompt += f"{filled_line()}\n"

        if exercise:
            prompt += f"The lesson contains {len(self.available())} available exercises.\n"
            prompt += f"{str(self.available())}\n" if self._show_available_on else ""
            prompt += "\n"
            prompt += str(exercise)
            prompt += "\n"

        prompt += "Do you want to:\n"

        if exercise:
            prompt += "  (a)nswer\n"
            prompt += "  (s)kip\n"

        prompt += "  (f)ind similar exercises\n"
        prompt += "  (c)reate a new exercise\n"

        if self._show_available_on:
            prompt += "  stop sho(w)ing all available exercises\n"
        else:
            prompt += "  start sho(w)ing all available exercises\n"

        prompt += "  (q)uit"

        return prompt

    def check_answer(self, exercise: Exercise, answer: str) -> str:
        # TODO: Return messages randomly picked from the pools of right/wrong messages.
        # TODO: Add an actual dictionary and use it to check solutions by replacing words and phrases.
        if clean(answer) == clean(exercise.solution):
            return "Correct!"
        # if check(self._dictionary, exercise, answer):
        #   return "Your answer is valid too."
        return "Wrong."

    def find_similar(self, base_exercise: Exercise) -> ExerciseManager:
        info = ask_exercise_info(self._EDIT_PROMPT, base_exercise)
        return self._exercise_pool.find(**info)

    def next_available(self) -> Exercise:
        return next((ex for ex in self._lesson if ex.is_available()), None)

    def next_available_index(self) -> int:
        return next((n for n, ex in enumerate(self._lesson) if ex.is_available()), 0)

    def refresh(self) -> None:
        self._lesson.refresh()

    def run_answer_line(self, exercise: Exercise) -> None:
        answer = input("Your answer: ")
        print(self.check_answer(exercise, answer))

        print(f"The intended answer was: {exercise.solution}")
        if ask("Mark the exercise as completed?"):
            exercise.make_completed()
        else:
            exercise.make_delayed()

    def run_create_line(self) -> None:
        info = ask_exercise_info(self._EDIT_PROMPT)
        self._lesson.add(Exercise(**info))

    def run_find_line(self, base_exercise: Exercise) -> None:
        found = self.find_similar(base_exercise)
        print_search_results(found)

        if not found:
            return

        current_index = self.next_available_index()
        print(self._ADD_PROMPT)
        to_add = parse_ranges(input())

        for index in to_add:
            try:
                exercise = found[index]
                exercise.make_available()
                self._lesson.insert(current_index, exercise)
                current_index += 1
            except IndexError:
                print(f"There is no item with the index #{index}.")

    def run_no_available_exercises_line(self) -> None:
        skipped = self.skipped()
        print("No available exercises left.")

        if not skipped:
            return

        print(f"There are {len(skipped)} skipped exercises.")
        if ask("Do you want to view them?"):
            self.refresh()

    def run_ui(self):
        while True:
            exercise = self.next_available()

            if not exercise:
                self.run_no_available_exercises_line()
                exercise = self.next_available()

            print(self.build_menu_prompt())

            option = input("Option: ").strip().lower()

            if option in ("q", "quit", "exit"):
                break

            # Answer/skip can only be done if there is an actual exercise to answer/skip.
            if exercise:
                if option in ("a", "answer"):
                    self.run_answer_line(exercise)
                if option in ("s", "skip"):
                    exercise.make_delayed()

            if option in ("f", "find"):
                self.run_find_line(exercise)

            if option in ("c", "create"):
                self.run_create_line()

            if option in ("w"):
                self._show_available_on = not self._show_available_on

    def skipped(self) -> ExerciseManager:
        return self._lesson.find(_status=Status.delayed)


if __name__ == "__main__":
    with Trainer("fi", "en") as tr:
        tr.run_ui()
