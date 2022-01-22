import pygame
from sys import exit

class Background:
    def __init__(self, screen, fileName: str, scale=None):
        try:
            self.img = pygame.image.load(fileName)
        except:
            print("Unable to load " + fileName)
            exit()
        if scale is not None:
            self.img = pygame.transform.scale(self.img, (scale))
        
        self.rect = self.img.get_rect()
        self.screen = screen
        
    def blit(self):
        self.screen.blit(self.img, self.rect)

