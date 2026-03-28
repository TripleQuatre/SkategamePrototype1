class Player:

  def __init__(self, id:str, name:str):
    self.id = id
    self.name = name
    self.status = "active"
    self.score = 0

  def receive_penalty(self):
        if self.is_eliminated():
            raise ValueError("eliminated player cannot receive a penalty")

        self.score += 1

  def eliminate(self):
    self.status = "eliminated"
  
  def is_eliminated(self):
    return self.status == "eliminated"
  
  def __repr__(self):
        return (
            f"Player(id={self.id}, name={self.name}, "
            f"status={self.status}, score={self.score})"
        )