from character import Character
import pygame


class Blair(Character):
    def __init__(self, screen):
        super().__init__(0, 0, screen, "blairrossetti.jpg")
