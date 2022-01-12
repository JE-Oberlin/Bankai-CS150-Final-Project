from character import Character
import inspect
import pygame


class Button():
    def __init__(self, screen, x=0, y=0, action=None, text="", buttonColor=(255, 255, 255), width=80, height=40,
                 size=18, textColor=(0, 0, 0), xOffset=10, yOffset=12, arg=None):
        pygame.init()
        self.screen = screen
        self.x = x
        self.y = y
        self.arg = arg
        print(self.arg)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = buttonColor
        self.font = pygame.font.SysFont("arial", size)
        self.text = text
        self.textColor = textColor
        self.renderedText = self.font.render(self.text, True, self.textColor)
        self.xOffset = xOffset
        self.yOffset = yOffset
        self._action = action

    def changeTextColor(self, col):
        self.text = self.font.render(self.text, True, col)

    def blit(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.renderedText, (self.x +
                         self.xOffset, self.y + self.yOffset))

    # This isn't confusing at all what do you mean bro
    def action(self):
        # print(self.arg)
        if self.arg is not None:
            self._action(self.arg)
        else:
            self._action()
