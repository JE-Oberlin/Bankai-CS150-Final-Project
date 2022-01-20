import pygame


class TextBox:
    def __init__(
        self,
        screen,
        textColor=(10, 10, 10),
        bkgndPos=(20, 350),
        bkgndSize=(660, 65),
        bkgndColor=(165, 211, 230),
        textOffsets=[(30, 375), (30, 355)],
    ):
        self.screen = screen
        self.character = ""
        self.text = ""
        self.font = pygame.font.SysFont("arial", 18)
        self.color = textColor
        self.dialogueText = self.font.render(self.text, True, self.color)
        self.characterText = self.font.render(self.character, True, self.color)
        self.bkgndRect = pygame.Rect(
            bkgndPos[0], bkgndPos[1], bkgndSize[0], bkgndSize[1]
        )
        self.bkgndColor = bkgndColor
        self.textOffsets = textOffsets

    def blit(self):
        pygame.draw.rect(self.screen, self.bkgndColor, self.bkgndRect)
        self.screen.blit(self.dialogueText, self.textOffsets[0])
        self.screen.blit(self.characterText, self.textOffsets[1])

    def updateText(self, text):
        # print(text)
        if type(text) is str:
            self.dialogueText = self.font.render(text, True, self.color)
            self.characterText = self.font.render("", True, self.color)
        elif len(text) > 1:
            self.dialogueText = self.font.render(text[1], True, self.color)
            if text[0] == "i":
                self.character = "Ichigo"
            elif text[0] == "a":
                self.character = "Aizen"
            elif text[0] == "n":
                self.character = ""
            else:
                self.character = text[0]

            self.characterText = self.font.render(self.character, True, self.color)
