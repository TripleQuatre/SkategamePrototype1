# engine/core.py

from typing import Optional
from .rules import GameRules  # import local, utile si on veut un fallback

class Player:
    """Représente un joueur de la partie."""
    def __init__(self, name: str):
        self.name = name
        self.is_attacker = False


class Game:
    """Représente une partie de Game of SKATE."""

    def __init__(self, rules: Optional[GameRules] = None):
        # si aucune règle fournie, on crée l'instance par défaut
        self.rules = rules or GameRules()
        self.apply_rules(self.rules)

        self.players = []
        self.current_attacker = None
        self.round = 1
        self.is_active = False

        # Règles utilisées par la partie (valeurs centralisées dans rules)
        #self.word = self.rules.word
        #self.max_attempts = self.rules.max_attempts

        # Suivi des lettres des joueurs (initialisé quand on ajoute les joueurs)
        self.letter_map = {}

    def add_player(self, player: Player):
        """Ajoute un joueur à la partie."""
        self.players.append(player)
        self.letter_map[player.name] = ""

    def start(self):
        """Démarre la partie."""
        if not self.players:
            raise ValueError("Impossible de démarrer : aucun joueur ajouté.")
        self.is_active = True
        self.current_attacker = self.players[0]
        self.current_attacker.is_attacker = True

    def next_turn(self):
        """Passe au joueur suivant."""
        if not self.is_active or not self.players:
            return

        if self.current_attacker not in self.players:
            next_idx = 0
        else:
            idx = self.players.index(self.current_attacker)
            next_idx = (idx + 1) % len(self.players)
            self.current_attacker.is_attacker = False

        self.current_attacker = self.players[next_idx]
        self.current_attacker.is_attacker = True
        self.round += 1

    def get_defenders(self):
        """Renvoie la liste des joueurs qui défendent."""
        return [p for p in self.players if p != self.current_attacker]

    def play_turn(self, attacker_success: bool, defenders_success: dict):
        """
        Simule un tour complet.
        :param attacker_success: bool, True si l'attaquant réussit sa figure
        :param defenders_success: dict {nom_joueur: bool}, réussite des défenseurs
        :return: dict avec le résumé du tour
        """
        if not self.is_active:
            raise RuntimeError("La partie n’a pas encore commencé.")

        results = {
            "attacker": self.current_attacker.name,
            "attacker_success": attacker_success,
            "defenders": {},
            "eliminated": []
        }

        # Si l'attaquant rate, on ne traite pas les défenseurs
        if not attacker_success:
            return results

        defenders = self.get_defenders()

        for d in list(defenders):  # list(...) car on peut modifier self.players pendant la boucle
            success = False
            # On lit la valeur fournie pour ce défenseur ; True par défaut si absent
            provided = defenders_success.get(d.name, True)
            # Si on veut supporter plusieurs essais fournis depuis l'extérieur,
            # defenders_success[d.name] pourrait être une liste. Pour l'instant on attend un bool.
            for attempt in range(1, self.max_attempts + 1):
                if provided:
                    success = True
                    break
                # si provided == False, on continue la boucle (simulate fails)
                # mais comme provided est une valeur fixe (issue du main), la boucle se contente
                # d'itérer self.max_attempts fois puis considère failure.
            if not success:
                current_len = len(self.letter_map[d.name])
                if current_len < len(self.word):
                    self.letter_map[d.name] += self.word[current_len]

                if len(self.letter_map[d.name]) >= len(self.word):
                    results["eliminated"].append(d.name)
                    # on retire le joueur éliminé de la liste de joueurs
                    try:
                        self.players.remove(d)
                    except ValueError:
                        pass

            results["defenders"][d.name] = {
                "success": success,
                "letters": self.letter_map[d.name]
            }

        # Si un seul joueur reste, fin de la partie
        if len(self.players) == 1:
            self.is_active = False
            results["winner"] = self.players[0].name

        return results

    def apply_rules(self, rules):
        """Applique un objet GameRules au jeu (met à jour les valeurs dérivées)."""
        self.rules = rules
        self.word = rules.word
        self.max_attempts = rules.max_attempts

        
