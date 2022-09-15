from __future__ import annotations

from base_ui import BaseUI
from exercise import Exercise
from exercise_manager import ExerciseManager
from interface import ask_exercise_info, filled_line, parse_ranges, print_search_results, repeat


class ExerciseBuilder(BaseUI):

    def build_menu_prompt(self) -> str:
        prompt = f"{filled_line()}\n"
        prompt += f"{filled_line('   MAIN MENU   ')}\n"
        prompt += f"{filled_line()}\n"

        prompt += "Do you want to:\n"

        if self._exercise_pool:
            prompt += f"  (v)iew exercises ({len(self._exercise_pool)} exercises total)\n"
            prompt += "  (r)emove exercises\n"

        prompt += "  (c)reate new exercises\n"
        prompt += "  (q)uit"

        return prompt

    def find(self) -> ExerciseManager:
        info = ask_exercise_info(self._EDIT_PROMPT)
        return self._exercise_pool.find(**info)

    def run_create_line(self) -> None:
        info = ask_exercise_info(self._EDIT_PROMPT)
        self._exercise_pool.add(Exercise(**info))

    def run_remove_line(self) -> None:
        found = self.find()
        print_search_results(found)
        print(self._REMOVE_PROMPT)

        for index in parse_ranges(input()):
            try:
                self._exercise_pool.remove(found[index])
            except IndexError:
                print(
                    f"Failed to remove the item #{index}: there is no such index.")

    def run_ui(self):
        while True:
            print(self.build_menu_prompt())

            option = input("Option: ").strip().lower()

            if option in ("q", "quit", "exit"):
                return

            if self._exercise_pool:
                if option in ("v", "view"):
                    repeat(self.run_view_line, "Look for another exercises?")
                if option in ("r", "rm", "remove"):
                    repeat(
                        self.run_remove_line, "The removal has been completed. Remove another exercises?")

            if option in ("c", "create"):
                repeat(
                    self.run_create_line, "The exercise has been successfully added. Add another exercise?")

    def run_view_line(self) -> None:
        found = self.find()
        print_search_results(found)


if __name__ == "__main__":
    with ExerciseBuilder("fi", "en") as eb:
        eb.run_ui()
