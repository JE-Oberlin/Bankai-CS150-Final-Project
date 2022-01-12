import character
import pygame

class MenuImg(character.Character):
  def __init__(self, screen):
    super().__init__(0, 100, screen, "bleach.png")
    self.image = pygame.transform.scale(self.image, (375, 81))