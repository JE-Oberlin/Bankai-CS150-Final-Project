import pygame


class TextBox:
    def __init__(
        self,
        screen,
        textColor=(10, 10, 10),
        bkgndPos=(20, 350),
        bkgndSize=(660, 65),
        bkgndColor=(165, 211, 230),
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
        self.charDict = {
            "i": "Ichigo",
            "a": "Aizen",
            "o": "Orehime",
            "r": "Rukia",
            "n": "",
            "b": "Blair Rossetti",
        }

    def blit(self):
        pygame.draw.rect(self.screen, self.bkgndColor, self.bkgndRect)
        self.screen.blit(
            self.dialogueText, (self.bkgndRect.left + 10, self.bkgndRect.top + 25)
        )
        self.screen.blit(
            self.characterText, (self.bkgndRect.left + 10, self.bkgndRect.top + 5)
        )

    def updateText(self, text):
        # print(text)
        if type(text) is str:
            self.dialogueText = self.font.render(text, True, self.color)
            self.characterText = self.font.render("", True, self.color)
        elif len(text) > 1:
            self.dialogueText = self.font.render(text[1], True, self.color)
            if text[0] in self.charDict.keys():
                self.character = self.charDict[text[0]]
            else:
                self.character = text[0]

            self.characterText = self.font.render(self.character, True, self.color)
