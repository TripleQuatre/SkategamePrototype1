import tkinter as tk
from tkinter import messagebox

from app.controller import GameController


class SkateGameUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("SkateGame Prototype")
        self.root.geometry("520x460")

        self.controller = GameController()

        self.player_names = []
        self.word = ""

        self.waiting_for_next_trick = False
        self.next_attacker_name = None

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

        self.build_game_screen()

        self.waiting_for_next_trick = True
        self.next_attacker_name = self.player_names[0]

        self.refresh_game_screen()

    def build_game_screen(self):
        self.clear_root()

        self.game_screen = tk.Frame(self.root, padx=20, pady=20)
        self.game_screen.pack(fill="both", expand=True)

        self.trick_input_frame = tk.Frame(self.game_screen)

        self.trick_prompt_label = tk.Label(
            self.trick_input_frame,
            font=("Arial", 12, "bold")
        )
        self.trick_prompt_label.pack(pady=(0, 8))

        self.trick_entry = tk.Entry(self.trick_input_frame, width=30)
        self.trick_entry.pack(pady=(0, 8))

        self.confirm_trick_button = tk.Button(
            self.trick_input_frame,
            text="Confirm trick",
            command=self.confirm_next_trick
        )
        self.confirm_trick_button.pack()

        self.players_label = tk.Label(
            self.game_screen,
            font=("Arial", 18, "bold")
        )
        self.players_label.pack(pady=(0, 15))

        self.score_frame = tk.Frame(self.game_screen)
        self.score_frame.pack(pady=(0, 25))

        self.left_word_frame = tk.Frame(self.score_frame)
        self.left_word_frame.pack(side="left", padx=(0, 25))

        self.separator_label = tk.Label(
            self.score_frame,
            text="-",
            font=("Arial", 18, "bold")
        )
        self.separator_label.pack(side="left")

        self.right_word_frame = tk.Frame(self.score_frame)
        self.right_word_frame.pack(side="left", padx=(25, 0))

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

        self.phase_label = tk.Label(
            self.game_screen,
            font=("Arial", 12)
        )
        self.phase_label.pack(pady=(0, 8))

        self.attempts_label = tk.Label(
            self.game_screen,
            font=("Arial", 12)
        )
        self.attempts_label.pack(pady=(0, 20))

        buttons_frame = tk.Frame(self.game_screen)
        buttons_frame.pack(pady=(0, 20))

        self.primary_button = tk.Button(
            buttons_frame,
            width=14,
            command=self.handle_primary_action
        )
        self.primary_button.pack(side="left", padx=10)

        self.secondary_button = tk.Button(
            buttons_frame,
            width=14,
            command=self.handle_secondary_action
        )
        self.secondary_button.pack(side="left", padx=10)

    def refresh_game_screen(self):
        if self.controller.is_finished():
            self.show_winner_screen()
            return

        self.players_label.config(
            text=f"{self.player_names[0].upper()} - {self.player_names[1].upper()}"
        )

        self.render_word_progress()

        if self.waiting_for_next_trick:
            self.turn_label.config(text="")
            self.trick_label.config(text="")
            self.phase_label.config(text="")
            self.attempts_label.config(text="")

            self.primary_button.config(text="", state="disabled")
            self.secondary_button.config(text="", state="disabled")

            self.trick_prompt_label.config(
                text=f"{self.next_attacker_name} sets the next trick"
            )
            self.trick_entry.delete(0, tk.END)
            self.trick_input_frame.pack(pady=(0, 20))
            self.trick_entry.focus_set()
            return

        turn = self.controller.get_current_turn()

        if turn is None:
            self.turn_label.config(text="")
            self.trick_label.config(text="")
            self.phase_label.config(text="")
            self.attempts_label.config(text="")

            self.primary_button.config(text="", state="disabled")
            self.secondary_button.config(text="", state="disabled")

            self.trick_prompt_label.config(text="")
            self.trick_input_frame.pack_forget()
            return

        attacker = turn.attacker
        defender = turn.defenders[0]

        self.trick_prompt_label.config(text="")
        self.trick_input_frame.pack_forget()

        self.turn_label.config(
            text=f"{attacker.name} attacks / {defender.name} defends"
        )
        self.trick_label.config(
            text=f"Trick: {turn.trick}"
        )

        if turn.turn_state == "attack_pending":
            self.phase_label.config(
                text=f"Attack phase: did {attacker.name} land the trick?"
            )
            self.attempts_label.config(text="")
            self.primary_button.config(text="Landed", state="normal")
            self.secondary_button.config(text="Missed", state="normal")

        elif turn.turn_state == "defense_pending":
            attempts_left = turn.defense_attempts_left[defender]

            self.phase_label.config(
                text=f"Defense phase: {defender.name} tries to reproduce the trick"
            )
            self.attempts_label.config(
                text=f"{defender.name} has {attempts_left} defense attempt(s) left"
            )
            self.primary_button.config(text="Success", state="normal")
            self.secondary_button.config(text="Failure", state="normal")

        else:
            self.phase_label.config(text="Unknown turn state")
            self.attempts_label.config(text="")
            self.primary_button.config(text="", state="disabled")
            self.secondary_button.config(text="", state="disabled")

    def render_word_progress(self):
        for widget in self.left_word_frame.winfo_children():
            widget.destroy()

        for widget in self.right_word_frame.winfo_children():
            widget.destroy()

        player1 = self.controller.players[self.player_names[0]]
        player2 = self.controller.players[self.player_names[1]]

        self.render_word_for_player(self.left_word_frame, player1.score)
        self.render_word_for_player(self.right_word_frame, player2.score)

    def confirm_next_trick(self):
        trick = self.trick_entry.get().strip()

        if not trick:
            messagebox.showerror("Invalid input", "Trick cannot be empty.")
            return

        try:
            if not self.controller.game.is_started:
                self.controller.start_game(self.next_attacker_name, trick)
            else:
                self.controller.prepare_next_turn(trick)
        except ValueError as error:
            messagebox.showerror("Trick error", str(error))
            return

        self.trick_entry.delete(0, tk.END)
        self.waiting_for_next_trick = False
        self.next_attacker_name = None

        self.refresh_game_screen()

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

    def handle_primary_action(self):
        turn = self.controller.get_current_turn()

        try:
            if turn.turn_state == "attack_pending":
                self.controller.resolve_attack(True)
                self.refresh_game_screen()

            elif turn.turn_state == "defense_pending":
                defender = turn.defenders[0]
                self.controller.resolve_defense(defender.name, "success")
                self.end_turn_and_continue()

        except ValueError as error:
            messagebox.showerror("Turn error", str(error))

    def handle_secondary_action(self):
        turn = self.controller.get_current_turn()

        try:
            if turn.turn_state == "attack_pending":
                self.controller.resolve_attack(False)
                self.end_turn_and_continue()

            elif turn.turn_state == "defense_pending":
                defender = turn.defenders[0]
                turn.use_defense_attempt(defender)

                if turn.defense_attempts_left[defender] == 0:
                    self.controller.resolve_defense(defender.name, "failure")
                    self.end_turn_and_continue()
                else:
                    self.refresh_game_screen()

        except ValueError as error:
            messagebox.showerror("Turn error", str(error))

    def end_turn_and_continue(self):
        try:
            self.controller.finish_turn()
        except ValueError as error:
            messagebox.showerror("Finish turn error", str(error))
            return

        if self.controller.is_finished():
            self.refresh_game_screen()
            return

        last_attacker = self.controller.game.turn_history[-1].attacker
        next_attacker = self.controller.game.get_next_attacker(last_attacker)

        self.waiting_for_next_trick = True
        self.next_attacker_name = next_attacker.name

        self.refresh_game_screen()

    def show_winner_screen(self):
        winner = self.controller.get_winner()

        self.render_word_progress()

        self.turn_label.config(text=f"Winner: {winner.name}")
        self.trick_label.config(text="")
        self.phase_label.config(text="")
        self.attempts_label.config(text="")

        self.primary_button.config(state="disabled")
        self.secondary_button.config(state="disabled")

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = SkateGameUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()