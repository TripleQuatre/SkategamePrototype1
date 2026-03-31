from app.controller import GameController


def ask_non_empty_text(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def ask_yes_no(prompt: str) -> str:
    while True:
        answer = input(prompt).strip().lower()

        if answer in ("y", "n"):
            return answer

        print("Please answer with y or n.")


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

    first_attacker = p1
    first_trick = ask_non_empty_text(f"{first_attacker} sets the first trick: ")
    controller.start_game(first_attacker, first_trick)

    while not controller.is_finished():
        turn = controller.get_current_turn()
        attacker = turn.attacker
        defender = turn.defenders[0]

        print(f"\n{attacker.name} vs {defender.name}")
        print(f"Trick: {turn.trick}")

        if turn.turn_state == "attack_pending":
            attack_answer = ask_yes_no(f"Did {attacker.name} land the trick? (y/n): ")
            controller.resolve_attack(attack_answer == "y")

            if turn.turn_state == "finished":
                previous_attacker = turn.attacker

                controller.finish_turn()
                display_scoreboard(controller)

                if controller.is_finished():
                    break

                next_attacker = controller.game.get_next_attacker(previous_attacker)
                next_trick = ask_non_empty_text(f"{next_attacker.name} sets the next trick: ")
                controller.prepare_next_turn(next_trick)
                continue

        while turn.turn_state == "defense_pending" and turn.defense_results[defender] is None:
            attempts_left = turn.defense_attempts_left[defender]
            print(f"{defender.name} has {attempts_left} attempt(s) left.")

            answer = ask_yes_no("Attempt successful? (y/n): ")

            if answer == "y":
                controller.resolve_defense(defender.name, "success")
            else:
                turn.use_defense_attempt(defender)

                if turn.defense_attempts_left[defender] == 0:
                    controller.resolve_defense(defender.name, "failure")
                else:
                    print("Attempt failed. Try again.")

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