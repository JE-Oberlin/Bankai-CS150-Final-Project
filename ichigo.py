from character import Character
from attack import Attack
import item
import pygame


class Ichigo(Character):
    def __init__(self, screen):
        super().__init__(0, 0, screen, "Ichigo.jpg")
        self.health = 1000
        self.MP = 200
        self.basicAttack = Attack("Attack", [45, 55], 95, 5)
        self.attacks = [Attack("Getsuga Tenshō", [200, 315], 85, 15)]
        self.inventory = {item.HealthItem(): 10}
        self.name = "Ichigo"
        self.holoified = False
        self.holoPoints = 0

    def swapPic(self):
        if self.holoified:
            self.image = pygame.image.load("holo.png")
            self.image = pygame.transform.scale(self.image, (350, 275))
        else:
            self.image = pygame.image.load("Ichigo.jpg")
            self.image = pygame.transform.scale(self.image, (350, 275))
