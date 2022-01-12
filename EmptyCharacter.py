import character
import pygame


class Empty(character.Character):
    def __init__(self, screen):
        super().__init__(0, 0, screen, "IMG_0646.jpg")
        self.image = pygame.transform.scale(self.image, (0, 0))
