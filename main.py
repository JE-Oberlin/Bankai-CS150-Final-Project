from GameManager import GameManager
import pygame
from sys import platform

pygame.init()
pygame.font.init()

# EVERYTHING HAPPENS IN GameManager CLASS


def main():
    gameManager = GameManager()

    gameManager.loop()


if __name__ == "__main__":
    main()
