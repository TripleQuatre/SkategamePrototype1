from app.controller import GameController


def run():
    controller = GameController()

    # Setup
    p1 = input("Player 1 name: ")
    p2 = input("Player 2 name: ")
    word = input("Word: ")
    attempts = int(input("Defense attempts (1-3): "))

    controller.create_game([p1, p2], word, attempts)

    attacker = p1
    first_trick = input(f"{attacker} sets the first trick: ")
    controller.start_game(attacker, first_trick)

    # Game loop
    while not controller.is_finished():
        turn = controller.get_current_turn()
        attacker = turn.attacker.name
        defender = turn.defenders[0].name

        print(f"\n{attacker} vs {defender}")
        print(f"Trick: {turn.trick}")

        result = input(f"{defender} success or failure? (s/f): ")

        if result == "s":
            controller.resolve_defense(defender, "success")
        else:
            controller.resolve_defense(defender, "failure")

        controller.finish_turn()

        if controller.is_finished():
            break

        next_trick = input("Next trick: ")
        controller.prepare_next_turn(next_trick)

    print(f"\nWinner is: {controller.get_winner().name}")

if __name__ == "__main__":
  run()