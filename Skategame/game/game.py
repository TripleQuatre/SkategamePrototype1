from player import Player
from settings import Settings
from turn import Turn


class Game:
    def __init__(self, players: list[Player], settings: Settings):
        self.players = players
        self.settings = settings
        self.current_turn = None
        self.turn_history = []
        self.is_started = False
        self.is_finished = False
        self.winner = None

    def start(self, first_attacker: Player, first_defenders: list[Player], trick: str):
        if self.is_started:
            raise ValueError("game has already started")

        if self.is_finished:
            raise ValueError("game is already finished")

        self.is_started = True
        self.create_turn(first_attacker, first_defenders, trick)

    def create_turn(self, attacker: Player, defenders: list[Player], trick: str):
        if not self.is_started:
            raise ValueError("game has not started yet")

        if self.is_finished:
            raise ValueError("game is already finished")

        self.current_turn = Turn(
            attacker,
            defenders,
            trick,
            self.settings.max_attempts_defense
        )

    def finish_current_turn(self):
        if self.current_turn is None:
            raise ValueError("there is no current turn to finish")

        self.turn_history.append(self.current_turn)
        self.current_turn = None

    def end_game(self, winner: Player):
        if self.is_finished:
            raise ValueError("game is already finished")

        self.winner = winner
        self.is_finished = True
        self.current_turn = None