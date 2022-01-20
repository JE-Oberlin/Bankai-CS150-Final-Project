import pygame
import random
import sys
import constants
import textBox
import EmptyCharacter
import util
import ScriptParser as sp
from button import Button
from ichigo import Ichigo
from aizen import Aizen
from attack import Attack
import item
import menuImg


class GameManager:
    screen = pygame.display.set_mode(constants.SIZE)

    def __init__(self):
        # pygame.init()
        # self.screen = pygame.display.set_mode(constants.SIZE)
        self.quitButton = Button(
            self.screen,
            680,
            375,
            self.quit,
            "Quit",
            width=40,
            height=20,
            size=10,
            xOffset=5,
            yOffset=6,
        )
        self.ichigo = Ichigo(self.screen)
        self.aizen = Aizen(self.screen)
        self.empty = EmptyCharacter.Empty(self.screen)
        self.mainMenuImg = menuImg.MenuImg(self.screen)
        self.mainMenuButtons = [
            Button(self.screen, 450, 100, self.start, "Start"),
            Button(self.screen, 450, 150, self.quit, "Quit"),
        ]
        self.deathButtons = [
            Button(self.screen, 450, 100, self.retryFight, "Retry?"),
            Button(self.screen, 450, 150, self.quit, "Quit"),
        ]
        self.fightButtons = [
            Button(
                self.screen,
                300,
                50,
                self.damageAizen,
                "Attack",
                arg=self.ichigo.basicAttack,
            ),
            Button(self.screen, 300, 100, self.skills, "Skills"),
            Button(self.screen, 300, 150, self.items, "Items"),
        ]
        self.textBox = textBox.TextBox(self.screen)
        self.healthBox = textBox.TextBox(
            self.screen,
            bkgndPos=(500, 200),
            bkgndSize=(100, 60),
            textOffsets=[(510, 225), (510, 205)],
        )
        self.healthText = str(self.ichigo.health) + "\n" + str(self.ichigo.MP)
        self.skillButtons = self.genSkillButtons()
        self.itemButtons = self.genItemButtons()
        self.updateText = "Click Start!"
        self.onScreenButtons = self.mainMenuButtons
        self.shownCharacter = self.mainMenuImg
        self.dialogueMode = False
        self.battleMode = False
        self.playerTurn = True
        self.ichigoAttacked = False
        self.timeToMurder = False
        self.timer = 0
        self.script = sp.ScriptParser("Script.txt")

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for b in self.onScreenButtons:
                        if b.rect.collidepoint(event.pos):
                            b.action()
                            if b.name == item.HealthItem.name:
                                self.itemButtons = self.genItemButtons()
                                del self.onScreenButtons[1:]
                                for a in self.itemButtons:
                                    self.onScreenButtons.append(a)
                    if self.dialogueMode:
                        # print(self.script.currentLine())
                        self.script.next()

            if self.battleMode:
                if self.ichigo.health <= 0:
                    del self.onScreenButtons
                    self.onScreenButtons = self.deathButtons
                    self.ichigoAttacked = False

                if self.aizen.health <= 0:
                    del self.onScreenButtons[1:]
                    self.battleMode = False
                    self.dialogueMode = True
                    self.ichigoAttacked = False

                if self.ichigoAttacked:
                    del self.onScreenButtons[1:]

                    self.timer += 1

                    if self.timeToMurder and self.timer > 3000:
                        self.damageIchigo()
                        self.timeToMurder = False

                    if self.timer > 5000:
                        for b in self.fightButtons:
                            self.onScreenButtons.append(b)

                        self.ichigoAttacked = False

                        self.timer = 0

                        self.updateText = "Please select what to do"
            elif self.dialogueMode:
                if self.script.currentLine()[0] == "i":
                    # print("Chingus")
                    self.shownCharacter = self.ichigo
                elif self.script.currentLine()[0] == "a":
                    self.shownCharacter = self.aizen
                # set up fight buttons
                elif self.script.currentLine()[0] == "<BATTLE>":
                    for b in self.fightButtons:
                        self.onScreenButtons.append(b)
                    self.battleMode = True
                    self.dialogueMode = False
                    self.updateText = ""
                    self.script.next()
                elif self.script.currentLine()[0] == "<END>":
                    # print("Hello there")
                    self.dialogueMode = False
                    self.battleMode = False
                    self.onScreenButtons = self.mainMenuButtons
                    self.shownCharacter = self.mainMenuImg
                    self.updateText = "Click Start!"
                    self.script.position = -1

            # print(self.shownCharacter)
            self.shownCharacter.move()

            self.screen.fill(constants.B_COLOR)
            self.shownCharacter.blit()
            # Display no buttons when Aizen is attacking
            for b in self.onScreenButtons:
                b.blit()
            if self.dialogueMode is True:
                self.textBox.updateText(self.script.currentLine())
            else:
                # print('HELLO')
                self.textBox.updateText(self.updateText)
                self.healthBox.updateText(
                    ["Health: " + str(self.ichigo.health), "MP: " + str(self.ichigo.MP)]
                )
            self.textBox.blit()
            if self.battleMode:
                self.healthBox.blit()
            pygame.display.flip()

    def genItemButtons(self):
        y = 50
        end = []
        for thing, n in self.ichigo.inventory.items():
            end.append(
                Button(
                    self.screen,
                    300,
                    y,
                    thing.use,
                    thing.name + " - " + str(n),
                    width=len(thing.name) * 18,
                    arg=[self.ichigo, self],
                    name=thing.name,
                )
            )
            y += 50

        end.append(
            Button(
                self.screen, 300, y, self.restoreButtons, "Back", arg=self.fightButtons
            )
        )

        return end

    def genSkillButtons(self):
        y = 50
        end = []
        for move in self.ichigo.attacks:
            end.append(
                Button(
                    self.screen,
                    300,
                    y,
                    self.damageAizen,
                    move.name,
                    width=len(move.name) * 11,
                    arg=move,
                )
            )
            y += 50

        end.append(
            Button(
                self.screen, 300, y, self.restoreButtons, "Back", arg=self.fightButtons
            )
        )

        return end

    def skills(self):
        # print(self.skillButtons)
        del self.onScreenButtons[1:]

        for b in self.skillButtons:
            self.onScreenButtons.append(b)

    def items(self):
        del self.onScreenButtons[1:]

        for b in self.itemButtons:
            self.onScreenButtons.append(b)

    def damageAizen(self, atk: Attack):
        c = random.randint(0, 100)

        self.ichigo.MP -= atk.cost

        if c > atk.hitChance:
            self.updateText = "Tried to use " + atk.name + ", but it missed!"
        else:
            d = random.randint(*atk.dmgRng)
            self.aizen.health -= d

            self.aizen.bump()

            self.updateText = "Aizen took " + str(d) + " damage!"

        self.ichigoAttacked = True
        self.timeToMurder = True

    def damageIchigo(self):
        c = random.randint(0, 100)

        sh = self.aizen.attacks[1]
        basic = self.aizen.attacks[0]

        if c < basic.useChance:
            # Use Basic
            c = random.randint(0, 100)
            self.aizen.MP -= basic.cost
            if c > basic.hitChance:
                self.updateText = (
                    "Aizen tried to use " + basic.name + ", but it missed!"
                )
            else:
                d = random.randint(*basic.dmgRng)

                self.ichigo.health -= d

                self.updateText = (
                    "Aizen used " + basic.name + " and you took " + str(d) + " damage!!"
                )
        else:
            # Use Shikai
            c = random.randint(0, 100)
            self.aizen.MP -= sh.cost
            if c > sh.hitChance:
                self.updateText = "Aizen tried to use " + sh.name + ", but it missed!"
            else:
                d = random.randint(*sh.dmgRng)

                self.ichigo.health -= d

                self.updateText = (
                    "Aizen used " + sh.name + " and you took " + str(d) + " damage!!"
                )

        # self.

    def changeShownCharacter(self, char):
        self.shownCharacter = char

    def restoreButtons(self, buttons: list):
        del self.onScreenButtons[1:]

        for b in buttons:
            self.onScreenButtons.append(b)

    def start(self):
        self.dialogueMode = True
        self.onScreenButtons = [self.quitButton]
        self.reset()

    def quit(self):
        sys.exit(23)

    def reset(self):
        self.ichigo.health = 500
        self.ichigo.MP = 150
        # This is actually the most disgusting thing I've ever done
        self.ichigo.inventory[util.cursedKeyGetter(self.ichigo.inventory, 0)] = 5

        self.aizen.health = 1000
        self.aizen.MP = 200

    def retryFight(self):
        self.reset()

        self.onScreenButtons = [self.quitButton] + self.fightButtons
