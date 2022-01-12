import pygame


class TextBox:
    def __init__(self, screen):
        self.screen = screen
        self.character = ""
        self.text = ""
        self.font = pygame.font.SysFont("arial", 18)
        self.color = (10, 10, 10)
        self.dialogueText = self.font.render(self.text, True, self.color)
        self.characterText = self.font.render(self.character, True, self.color)
        self.bkgndRect = pygame.Rect(20, 350, 660, 65)

    def blit(self):
        pygame.draw.rect(self.screen, (165, 211, 230), self.bkgndRect)
        self.screen.blit(self.dialogueText, (30, 375))
        self.screen.blit(self.characterText, (30, 355))

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
            else:
                self.character = ""

            self.characterText = self.font.render(
                self.character, True, self.color)
