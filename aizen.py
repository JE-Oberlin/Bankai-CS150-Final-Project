from character import Character
from attack import Attack
import pygame


class Aizen(Character):
    # need use chances for the "AI", more like Artificial Dumbness lol.
    class Shikai(Attack):
        def __init__(self):
            super().__init__('Shikai - "Kyōka Suigetsu"', [250, 390], 60, 30)
            self.useChance = 35

    class BasicAttack(Attack):
        def __init__(self):
            super().__init__("Attack", [50, 80], 80, 10)
            self.useChance = 65

    def __init__(self, screen):
        super().__init__(0, 0, screen, "aizen.png")
        self.health = 2500
        self.MP = 250
        self.attacks = [Aizen.BasicAttack(), Aizen.Shikai()]
