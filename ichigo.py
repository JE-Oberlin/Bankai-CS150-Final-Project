from character import Character
from attack import Attack
import item
import pygame


class Ichigo(Character):
  def __init__(self, screen):
    super().__init__(0, 0, screen, "IchigoKurosakiBleach.jpg")
    self.image = pygame.transform.scale(self.image, (275, 275))
    self.health = 500
    self.MP = 150
    self.basicAttack = Attack("Attack", [45, 55], 95, 5)
    self.attacks = [Attack("Getsuga Tenshō", [200, 315], 85, 15)]
    self.inventory = {item.HealthItem: 5}
    