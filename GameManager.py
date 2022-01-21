import pygame
import random
import sys
import constants
import textBox
import EmptyCharacter
import util
import ScriptParser as sp
import sounds

# I do this because I am lazy, don't judge me.
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
        self.inMainMenu = True
        self.playingMenuMusic = False
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
            self.screen, bkgndPos=(500, 250), bkgndSize=(120, 60)
        )
        self.aizenBox = textBox.TextBox(
            self.screen, bkgndPos=(60, 280), bkgndSize=(165, 60)
        )
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

            if self.inMainMenu and not self.playingMenuMusic:
                pygame.mixer.Sound.play(sounds.menuMusic)
                self.playingMenuMusic = True
            elif not self.inMainMenu and self.playingMenuMusic:
                pygame.mixer.Sound.stop(sounds.menuMusic)
                self.playingMenuMusic = False

            if self.battleMode:
                if self.ichigo.health <= 0:
                    del self.onScreenButtons
                    pygame.mixer.Sound.stop(sounds.fight)
                    self.onScreenButtons = self.deathButtons
                    self.ichigoAttacked = False

                if self.aizen.health <= 0:
                    del self.onScreenButtons[1:]
                    pygame.mixer.Sound.stop(sounds.fight)
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
                    self.shownCharacter = self.ichigo
                elif self.script.currentLine()[0] == "a":
                    self.shownCharacter = self.aizen
                elif self.script.currentLine()[0] == "show":
                    if self.script.currentLine()[1] == "i":
                        self.shownCharacter = self.ichigo
                    elif self.script.currentLine()[1] == "a":
                        self.shownCharacter = self.aizen

                    self.script.next()
                elif self.script.currentLine()[0] == "<BATTLE>":
                    for b in self.fightButtons:
                        self.onScreenButtons.append(b)
                    self.battleMode = True
                    self.dialogueMode = False
                    self.updateText = "Please select what to do"
                    pygame.mixer.Sound.play(sounds.fight)
                    self.script.next()
                elif self.script.currentLine()[0] == "<END>":
                    # print("Hello there")
                    self.dialogueMode = False
                    self.battleMode = False
                    self.onScreenButtons = self.mainMenuButtons
                    self.shownCharacter = self.mainMenuImg
                    self.inMainMenu = True
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
                self.aizenBox.updateText("Aizen Health: " + str(self.aizen.health))
            self.textBox.blit()
            if self.battleMode:
                self.healthBox.blit()
                self.aizenBox.blit()
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
        self.inMainMenu = False
        self.onScreenButtons = [self.quitButton]
        self.reset()

    def quit(self):
        sys.exit(23)

    def reset(self):
        self.ichigo.health = 500
        self.ichigo.MP = 150
        # This is actually the most disgusting thing I've ever done
        # self.ichigo.inventory[util.cursedKeyGetter(self.ichigo.inventory, 0)] = 5
        # HAHA I MADE IT WORSE!
        self.ichigo.inventory[[x for x in self.ichigo.inventory.keys()][0]] = 5
        self.aizen.health = 1000
        self.aizen.MP = 200

    def retryFight(self):
        self.reset()

        self.onScreenButtons = [self.quitButton] + self.fightButtons
        pygame.mixer.Sound.play(sounds.fight)
