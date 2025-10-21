# engine/rules.py

import json
from pathlib import Path
from typing import Any, Dict

RULES_DIR = Path("rulesets")
RULES_DIR.mkdir(exist_ok=True)


class GameRules:
    """Objet contenant les règles de la partie (simplifié)."""

    def __init__(self, name: str = "Standard SKATE", 
                 word: str = "SKATE", max_attempts: int = 3, 
                 player_order: str = "default"):
        self.name = name
        self.word = word
        self.max_attempts = max_attempts
        self.player_order = player_order

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "word": self.word,
            "max_attempts": self.max_attempts,
            "player_order": self.player_order
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            name=data.get("name", "Custom"),
            word=data.get("word", "SKATE"),
            max_attempts=int(data.get("max_attempts", 3)),
            player_order=data.get("player_order", "default")
        )

    def update_rule(self, key: str, value: Any):
        """Permet de modifier une règle individuellement."""
        if not hasattr(self, key):
            raise KeyError(f"Règle inconnue : {key}")
        setattr(self, key, value)

    def save(self, filename: str):
        """Sauvegarde la règle dans rulesets/<filename>.json"""
        path = RULES_DIR / f"{filename}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @staticmethod
    def load(filename: str):
        """Charge une règle depuis rulesets/<filename>.json"""
        path = RULES_DIR / f"{filename}.json"
        if not path.exists():
            raise FileNotFoundError(f"{path} introuvable")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return GameRules.from_dict(data)


# PRESET minimal (le SKATE classique)
PRESET_RULES = {
    "Standard SKATE": GameRules(name="Standard SKATE", 
                                word="SKATE", 
                                max_attempts=3, 
                                player_order="random")
}
