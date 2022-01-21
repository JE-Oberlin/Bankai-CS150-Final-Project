from GameManager import GameManager
import pygame
from sys import platform

pygame.init()
pygame.font.init()

# EVERYTHING HAPPENS IN GameManager CLASS

# Hello there


def main():
    gameManager = GameManager()

    gameManager.loop()


if __name__ == "__main__":
    main()
