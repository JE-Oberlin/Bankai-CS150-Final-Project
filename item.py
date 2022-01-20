from character import Character


class Item:
    def __init__(self):
        self.name = ""

    def use(self):
        pass


class HealthItem(Item):
    def __init__(self):
        self.name = "Bandage"

    def use(self, character: Character):
        character.health += 75
