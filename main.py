from GameManager import GameManager
import pygame

pygame.init()
pygame.font.init()

# EVERYTHING HAPPENS IN GameManager CLASS


def main():
    # pygame.init()

    gameManager = GameManager()

    # gameManager.changeShownCharacter(gameManager.aizen)

    gameManager.loop()


if __name__ == "__main__":
    main()
