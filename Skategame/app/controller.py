from game.game import Game
from game.player import Player
from game.settings import Settings


class GameController:
    def __init__(self):
        self.game = None
        self.players = {}

    def create_game(self, player_names, word, max_defense_attempts):
        self.players = {}
        players = []
        for i, name in enumerate(player_names):
            player = Player(i, name)
            players.append(player)
            self.players[name] = player

        settings = Settings(word, 1, max_defense_attempts)
        self.game = Game(players, settings)

    def start_game(self, attacker_name, trick):
        attacker = self.players[attacker_name]
        defenders = [p for p in self.game.players if p != attacker]

        self.game.start(attacker, defenders, trick)

    def resolve_attack(self, success: bool):
        if self.game.current_turn is None:
            raise ValueError("no current turn")

        turn = self.game.current_turn

        if success:
            turn.set_attack_success()
        else:
            turn.set_attack_failure()

    def resolve_defense(self, defender_name, result):
        defender = self.players[defender_name]

        if result == "success":
            self.game.current_turn.set_defense_success(defender)
        else:
            self.game.current_turn.set_defense_failure(defender)

    def finish_turn(self):
        self.game.finish_current_turn()

    def prepare_next_turn(self, trick):
        current_attacker_name = self.game.turn_history[-1].attacker
        current_attacker = self.players[current_attacker_name]
        next_attacker = self.game.get_next_attacker(current_attacker)
        self.game.prepare_next_turn(next_attacker, trick)

    def is_finished(self):
        return self.game.is_finished

    def get_winner(self):
        return self.game.winner

    def get_current_turn(self):
        return self.game.current_turn