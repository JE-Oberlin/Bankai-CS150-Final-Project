from character import Character
import pygame


class Rukia(Character):
    def __init__(self, screen):
        super().__init__(0, 0, screen, "rukia.png")
        self.image = pygame.transform.scale(self.image, (275, 275))
