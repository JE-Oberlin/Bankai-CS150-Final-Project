import pygame
import sys
import constants
from attack import Attack
import random

class Character:
  def __init__(self, x, y, screen, imagePath: str):
    self.screen = screen

    try:
      self.image = pygame.image.load(imagePath)
    except:
      print("Could not load " + imagePath)
      sys.exit(69)

    self.rect = self.image.get_rect()
    self.pos = x, y
    self.bumped = False
    self.tslb = 0 # time since last bump

    # Attack objects
    self.attacks = []
    self.whenHit = [] # lines said when hit
    self.whenAtk = [] # lines said when attacking

    self.health = None
    self.MP = None

  def blit(self):
    self.screen.blit(self.image, self.rect)

  def bump(self):
    self.pos = 0, 10
    self.bumped = True

  # override in child classes
  def update(self):
    if self.bumped and self.tslb < 500:
      self.tslb += 1
    elif self.bumped:
      self.tslb = 0
      self.pos = 0, -10
      self.bumped = False

  def move(self):
    self.update()
    self.rect = self.rect.move(self.pos)
    self.pos = 0, 0

  def attack(self):
    return random.choice(self.attacks)