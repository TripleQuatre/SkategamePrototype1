import tkinter as tk
from tkinter import messagebox

from app.controller import GameController


class SkateGameUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("SkateGame Prototype")
        self.root.geometry("420x360")

        self.controller = GameController()

        self.player_names = []
        self.word = ""

        self.setup_screen = None
        self.game_screen = None

        self.build_setup_screen()

    def build_setup_screen(self):
        self.clear_root()

        self.setup_screen = tk.Frame(self.root, padx=20, pady=20)
        self.setup_screen.pack(fill="both", expand=True)

        title_label = tk.Label(
            self.setup_screen,
            text="SkateGame Setup",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))

        tk.Label(self.setup_screen, text="Player 1 name:").pack(anchor="w")
        self.player1_entry = tk.Entry(self.setup_screen)
        self.player1_entry.pack(fill="x", pady=(0, 10))

        tk.Label(self.setup_screen, text="Player 2 name:").pack(anchor="w")
        self.player2_entry = tk.Entry(self.setup_screen)
        self.player2_entry.pack(fill="x", pady=(0, 10))

        tk.Label(self.setup_screen, text="Word:").pack(anchor="w")
        self.word_entry = tk.Entry(self.setup_screen)
        self.word_entry.pack(fill="x", pady=(0, 10))

        tk.Label(self.setup_screen, text="Defense attempts:").pack(anchor="w")

        self.attempts_var = tk.IntVar(value=1)

        attempts_frame = tk.Frame(self.setup_screen)
        attempts_frame.pack(anchor="w", pady=(0, 20))

        tk.Radiobutton(
            attempts_frame, text="1", variable=self.attempts_var, value=1
        ).pack(side="left", padx=(0, 10))

        tk.Radiobutton(
            attempts_frame, text="2", variable=self.attempts_var, value=2
        ).pack(side="left", padx=(0, 10))

        tk.Radiobutton(
            attempts_frame, text="3", variable=self.attempts_var, value=3
        ).pack(side="left")

        start_button = tk.Button(
            self.setup_screen,
            text="Start game",
            command=self.start_game_flow,
            width=16
        )
        start_button.pack(pady=(10, 0))

    def start_game_flow(self):
        player1 = self.player1_entry.get().strip()
        player2 = self.player2_entry.get().strip()
        word = self.word_entry.get().strip().upper()
        attempts = self.attempts_var.get()

        if not player1 or not player2 or not word:
            messagebox.showerror("Invalid input", "All fields are required.")
            return

        try:
            self.controller.create_game([player1, player2], word, attempts)
        except ValueError as error:
            messagebox.showerror("Invalid game settings", str(error))
            return

        self.player_names = [player1, player2]
        self.word = word

        first_attacker = self.player_names[0]

        first_trick = self.ask_text_dialog(f"{first_attacker} sets the first trick:")
        if first_trick is None:
            return

        try:
            self.controller.start_game(first_attacker, first_trick)
        except ValueError as error:
            messagebox.showerror("Start error", str(error))
            return

        self.build_game_screen()
        self.refresh_game_screen()

    def build_game_screen(self):
        self.clear_root()

        self.game_screen = tk.Frame(self.root, padx=20, pady=20)
        self.game_screen.pack(fill="both", expand=True)

        # Header players
        self.players_label = tk.Label(
            self.game_screen,
            font=("Arial", 18, "bold")
        )
        self.players_label.pack(pady=(0, 15))

        # Score word area
        self.score_frame = tk.Frame(self.game_screen)
        self.score_frame.pack(pady=(0, 25))

        self.left_word_frame = tk.Frame(self.score_frame)
        self.left_word_frame.pack(side="left", padx=(0, 30))

        self.separator_label = tk.Label(
            self.score_frame,
            text="-",
            font=("Arial", 18, "bold")
        )
        self.separator_label.pack(side="left")

        self.right_word_frame = tk.Frame(self.score_frame)
        self.right_word_frame.pack(side="left", padx=(30, 0))

        # Turn info
        self.turn_label = tk.Label(
            self.game_screen,
            font=("Arial", 14, "bold")
        )
        self.turn_label.pack(pady=(0, 10))

        self.trick_label = tk.Label(
            self.game_screen,
            font=("Arial", 13)
        )
        self.trick_label.pack(pady=(0, 10))

        self.attempts_label = tk.Label(
            self.game_screen,
            font=("Arial", 12)
        )
        self.attempts_label.pack(pady=(0, 20))

        # Buttons
        buttons_frame = tk.Frame(self.game_screen)
        buttons_frame.pack(pady=(0, 20))

        self.success_button = tk.Button(
            buttons_frame,
            text="Success",
            width=14,
            command=self.handle_success
        )
        self.success_button.pack(side="left", padx=10)

        self.fail_button = tk.Button(
            buttons_frame,
            text="Fail attempt",
            width=14,
            command=self.handle_fail_attempt
        )
        self.fail_button.pack(side="left", padx=10)

    def refresh_game_screen(self):
        game = self.controller.game

        if game.is_finished:
            self.show_winner_screen()
            return

        turn = self.controller.get_current_turn()
        attacker = turn.attacker
        defender = turn.defenders[0]

        self.players_label.config(
            text=f"{self.player_names[0].upper()} - {self.player_names[1].upper()}"
        )

        self.render_word_progress()

        self.turn_label.config(
            text=f"{attacker.name} attacks / {defender.name} defends"
        )

        self.trick_label.config(
            text=f"Trick: {turn.trick}"
        )

        attempts_left = turn.defense_attempts_left[defender]
        self.attempts_label.config(
            text=f"{defender.name} has {attempts_left} defense attempt(s) left"
        )

    def render_word_progress(self):
        for widget in self.left_word_frame.winfo_children():
            widget.destroy()

        for widget in self.right_word_frame.winfo_children():
            widget.destroy()

        player1 = self.controller.players[self.player_names[0]]
        player2 = self.controller.players[self.player_names[1]]

        self.render_word_for_player(self.left_word_frame, player1.score)
        self.render_word_for_player(self.right_word_frame, player2.score)

    def render_word_for_player(self, parent_frame, score: int):
        for index, letter in enumerate(self.word):
            if index < score:
                label = tk.Label(
                    parent_frame,
                    text=letter,
                    font=("Arial", 20, "bold"),
                    fg="black"
                )
            else:
                label = tk.Label(
                    parent_frame,
                    text=letter,
                    font=("Arial", 20),
                    fg="gray"
                )

            label.pack(side="left", padx=2)

    def handle_success(self):
        turn = self.controller.get_current_turn()
        defender = turn.defenders[0]

        try:
            self.controller.resolve_defense(defender.name, "success")
            self.end_turn_and_continue()
        except ValueError as error:
            messagebox.showerror("Turn error", str(error))

    def handle_fail_attempt(self):
        turn = self.controller.get_current_turn()
        defender = turn.defenders[0]

        try:
            turn.use_defense_attempt(defender)

            if turn.defense_attempts_left[defender] == 0:
                self.controller.resolve_defense(defender.name, "failure")
                self.end_turn_and_continue()
            else:
                self.refresh_game_screen()

        except ValueError as error:
            messagebox.showerror("Turn error", str(error))

    def end_turn_and_continue(self):
        turn = self.controller.get_current_turn()
        previous_attacker = turn.attacker

        try:
            self.controller.finish_turn()
        except ValueError as error:
            messagebox.showerror("Finish turn error", str(error))
            return

        if self.controller.is_finished():
            self.refresh_game_screen()
            return

        next_attacker = self.controller.game.get_next_attacker(previous_attacker)
        next_trick = self.ask_text_dialog(f"{next_attacker.name} sets the next trick:")

        if next_trick is None:
            return

        try:
            self.controller.prepare_next_turn(next_trick)
        except ValueError as error:
            messagebox.showerror("Next turn error", str(error))
            return

        self.refresh_game_screen()

    def show_winner_screen(self):
        winner = self.controller.get_winner()

        self.turn_label.config(text=f"Winner: {winner.name}")
        self.trick_label.config(text="")
        self.attempts_label.config(text="")

        self.success_button.config(state="disabled")
        self.fail_button.config(state="disabled")

        self.render_word_progress()

    def ask_text_dialog(self, prompt: str):
        dialog = tk.Toplevel(self.root)
        dialog.title("Input")
        dialog.geometry("320x140")
        dialog.transient(self.root)
        dialog.grab_set()

        result = {"value": None}

        tk.Label(dialog, text=prompt, wraplength=280).pack(pady=(15, 10))

        entry = tk.Entry(dialog)
        entry.pack(fill="x", padx=20)
        entry.focus_set()

        def validate():
            value = entry.get().strip()
            if not value:
                messagebox.showerror("Invalid input", "This field cannot be empty.", parent=dialog)
                return
            result["value"] = value
            dialog.destroy()

        def cancel():
            dialog.destroy()

        buttons_frame = tk.Frame(dialog)
        buttons_frame.pack(pady=15)

        tk.Button(buttons_frame, text="OK", width=10, command=validate).pack(side="left", padx=5)
        tk.Button(buttons_frame, text="Cancel", width=10, command=cancel).pack(side="left", padx=5)

        dialog.wait_window()
        return result["value"]

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()


def main():
    root = tk.Tk()
    app = SkateGameUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()