class Attack:
  # dr should be in form [low, high]
  def __init__(self, name, dr, hit, cost):
    self.dmgRng = dr
    self.cost = cost
    self.name = name
    self.hitChance = hit