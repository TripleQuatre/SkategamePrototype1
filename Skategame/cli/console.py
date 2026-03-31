from app.controller import GameController


def ask_non_empty_text(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def ask_defense_attempts() -> int:
    while True:
        raw_value = input("Defense attempts (1-3): ").strip()

        if not raw_value.isdigit():
            print("Please enter a number between 1 and 3.")
            continue

        attempts = int(raw_value)

        if 1 <= attempts <= 3:
            return attempts

        print("Defense attempts must be between 1 and 3.")

def format_word_progress(word: str, score: int) -> str:
    revealed = []

    for index, letter in enumerate(word):
        if index < score:
            revealed.append(letter)
        else:
            revealed.append("_")

    return " ".join(revealed)


def display_scoreboard(controller):
    word = controller.game.settings.word

    print("\nScore:")
    for player in controller.game.players:
        progress = format_word_progress(word, player.score)
        print(f"{player.name:<10} {progress}")

def run():
    controller = GameController()

    p1 = ask_non_empty_text("Player 1 name: ")
    p2 = ask_non_empty_text("Player 2 name: ")
    word = ask_non_empty_text("Word: ")
    attempts = ask_defense_attempts()

    controller.create_game([p1, p2], word, attempts)

    attacker = p1
    first_trick = ask_non_empty_text(f"{attacker} sets the first trick: ")
    controller.start_game(attacker, first_trick)

    while not controller.is_finished():
        turn = controller.get_current_turn()
        attacker_name = turn.attacker.name
        defender = turn.defenders[0]

        print(f"\n{attacker_name} vs {defender.name}")
        print(f"Trick: {turn.trick}")

        while turn.defense_results[defender] is None:
            attempts_left = turn.defense_attempts_left[defender]
            print(f"{defender.name} has {attempts_left} attempt(s) left.")

            answer = input(
                f"Attempt successful? (y/n): "
            ).strip().lower()

            if answer not in ("y", "n"):
                print("Please answer with y or n.")
                continue

            if answer == "y":
                controller.resolve_defense(defender.name, "success")
            else:
                turn.use_defense_attempt(defender)

                if turn.defense_attempts_left[defender] == 0:
                    controller.resolve_defense(defender.name, "failure")
                else:
                    print("Attempt failed. Try again.")

        if controller.is_finished():
            break

        previous_attacker = turn.attacker

        controller.finish_turn()
        display_scoreboard(controller)

        if controller.is_finished():
          break

        next_attacker = controller.game.get_next_attacker(previous_attacker)
        next_trick = ask_non_empty_text(f"{next_attacker.name} sets the next trick: ")

        controller.prepare_next_turn(next_trick)

    print(f"\nWinner is: {controller.get_winner().name}")

if __name__ == "__main__":
    run()