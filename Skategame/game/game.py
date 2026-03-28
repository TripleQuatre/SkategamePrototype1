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

        if self.current_turn is not None:
            raise ValueError("a turn is already in progress")

        self.current_turn = Turn(
            attacker,
            defenders,
            trick,
            self.settings.max_attempts_defense
        )

    def get_active_players(self):
        return [player for player in self.players if not player.is_eliminated()]

    def finish_current_turn(self):
        if self.current_turn is None:
            raise ValueError("there is no current turn to finish")

        if not self.current_turn.is_finished():
            raise ValueError("current turn is not finished")

        finished_turn = self.current_turn

        for defender, result in finished_turn.result.items():
            if result == "failure":
                defender.receive_penalty()

                if self.settings.should_eliminate(defender.score):
                    defender.eliminate()

        self.check_winner()

        self.turn_history.append(finished_turn)
        self.current_turn = None

    def check_winner(self):
        active_players = self.get_active_players()

        if len(active_players) == 1:
            self.end_game(active_players[0])
            return active_players[0]

        return None

    def get_next_attacker(self, current_attacker: Player):
        active_players = self.get_active_players()

        current_index = active_players.index(current_attacker)
        next_index = (current_index + 1) % len(active_players)

        return active_players[next_index]

    def prepare_next_turn(self, attacker: Player, trick: str):
        if not self.is_started:
            raise ValueError("game has not started yet")

        if self.is_finished:
            raise ValueError("game is already finished")

        if self.current_turn is not None:
            raise ValueError("current turn must be finished before preparing a new one")

        active_players = self.get_active_players()

        if attacker not in active_players:
            raise ValueError("attacker must be an active player")

        defenders = [player for player in active_players if player != attacker]

        if len(defenders) == 0:
            raise ValueError("not enough players to create a turn")

        self.create_turn(attacker, defenders, trick)

    def end_game(self, winner: Player):
        if self.is_finished:
            raise ValueError("game is already finished")

        self.winner = winner
        self.is_finished = True
        self.current_turn = None