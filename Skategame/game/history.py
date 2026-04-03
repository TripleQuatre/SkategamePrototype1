class TurnRecord:
    def __init__(
        self,
        turn_number: int,
        attacker: str,
        trick: str,
        attack_result: str,
        letters_received: list[str],
        eliminated_players: list[str],
        defense_attempts: dict[str, list[str]]
    ):
        self.turn_number = turn_number
        self.attacker = attacker
        self.trick = trick
        self.attack_result = attack_result
        self.letters_received = letters_received
        self.eliminated_players = eliminated_players
        self.defense_attempts = defense_attempts

    def __repr__(self):
        return (
            f"Turn {self.turn_number} | "
            f"{self.attacker} -> '{self.trick}' | "
            f"attack: {self.attack_result} | "
            f"defense: {self.defense_attempts} | "
            f"letters: {self.letters_received} | "
            f"eliminated: {self.eliminated_players}"
        )
    
