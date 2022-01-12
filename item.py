from character import Character

class HealthItem:
  def __init__(self):
    self.name = "Bandage"

  def use(self, character: Character):
    character.health += 75