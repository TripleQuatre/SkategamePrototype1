class Settings:

  def __init__(self, word: str, max_attempts_attack: int, max_attempts_defense: int):
    if not word:
      raise ValueError("word cannot be empty")
    
    if len(word) > 10:
      raise ValueError("word cannot be more than 10 letters")
    
    if max_attempts_attack != 1:
      raise ValueError("attack attempts must be equal to 1")
    
    if max_attempts_defense < 1 or max_attempts_defense > 3:
      raise ValueError("defense attempts must be between 1 and 3")

    self.word = word
    self.max_attempts_attack = max_attempts_attack 
    self.max_attempts_defense = max_attempts_defense

  def should_eliminate(self, score: int) -> bool:
      return score >= len(self.word)
