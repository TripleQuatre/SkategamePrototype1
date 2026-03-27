from player import Player


class Turn:
    def __init__(self,
        attacker: Player,
        defenders: list[Player],
        trick: str,
        max_defense_attempts: int
    ):
        self.attacker = attacker
        self.defenders = defenders
        self.trick = trick
        self.max_defense_attempts = max_defense_attempts

        self.defense_attempts_left = {
            defender: max_defense_attempts for defender in defenders
        }

        self.defense_results = {
            defender: None for defender in defenders
        }

        self.turn_state = "defense_pending"
        self.result = None

    def use_defense_attempt(self, defender: Player):
        if self.turn_state != "defense_pending":
            raise ValueError("defense is not pending")

        if defender not in self.defenders:
            raise ValueError("defender is not part of this turn")

        if self.defense_results[defender] is not None:
            raise ValueError("this defender already has a result")

        if self.defense_attempts_left[defender] <= 0:
            raise ValueError("no defense attempts left for this defender")

        self.defense_attempts_left[defender] -= 1

    def set_defense_success(self, defender: Player):
        if self.turn_state != "defense_pending":
            raise ValueError("defense is not pending")

        if defender not in self.defenders:
            raise ValueError("defender is not part of this turn")

        if self.defense_results[defender] is not None:
            raise ValueError("this defender already has a result")

        self.defense_results[defender] = "success"
        self.update_turn_state()

    def set_defense_failure(self, defender: Player):
        if self.turn_state != "defense_pending":
            raise ValueError("defense is not pending")

        if defender not in self.defenders:
            raise ValueError("defender is not part of this turn")

        if self.defense_results[defender] is not None:
            raise ValueError("this defender already has a result")

        self.defense_results[defender] = "failure"
        self.update_turn_state()

    def all_defenders_answered(self):
        return all(result is not None for result in self.defense_results.values())

    def update_turn_state(self):
        if self.all_defenders_answered():
            self.turn_state = "finished"
            self.result = self.defense_results.copy()

    def is_finished(self):
        return self.turn_state == "finished"