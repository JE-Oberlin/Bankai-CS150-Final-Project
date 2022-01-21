from character import Character


class Item:
    def __init__(self):
        self.name = ""

    def use(self):
        pass


class HealthItem(Item):
    name = "Bandage"

    def __init__(self):
        self.name = "Bandage"

    def use(self, stuff: list):
        # print("Hello there")
        if stuff[0].health >= 500:
            stuff[1].updateText = "You are at full health, no healing for you!"
        elif stuff[0].inventory[self] > 0:
            stuff[0].health += 75
            stuff[1].updateText = stuff[0].name + " gets 75 health back!"
            stuff[0].inventory[self] -= 1
        else:
            stuff[1].updateText = 'You are out of "Bandages"!'
