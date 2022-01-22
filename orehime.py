from character import Character
import pygame


class Orehime(Character):
    def __init__(self, screen):
        super().__init__(0, 0, screen, "orihime.png")
        self.image = pygame.transform.scale(self.image, (350, 275))
