import pygame
import random
import sys
import constants
import textBox
import EmptyCharacter
import ScriptParser as sp
from button import Button
from ichigo import Ichigo
from aizen import Aizen
from attack import Attack
import menuImg



class GameManager:
  screen = pygame.display.set_mode(constants.SIZE)
  def __init__(self):
    #pygame.init()
    #self.screen = pygame.display.set_mode(constants.SIZE)
    self.quitButton = Button(self.screen, 680, 375, self.quit, "Quit", width=40, height=20, size=10, xOffset=5, yOffset=6)
    self.ichigo = Ichigo(self.screen)
    self.aizen = Aizen(self.screen)
    self.empty = EmptyCharacter.Empty(self.screen)
    self.mainMenuImg = menuImg.MenuImg(self.screen)
    self.mainMenuButtons = [Button(self.screen, 450, 100,
                            self.start, "Start"), 
                            Button(self.screen, 450, 150, self.quit, "Quit")]
    self.fightButtons = [Button(self.screen, 300, 50,            
                        self.damageAizen, "Attack", arg=self.ichigo.basicAttack),
                        Button(self.screen, 300, 100,
                        self.skills, "Skills")]
    self.skillButtons = self.genSkillButtons()
    self.itemButtons = []
    self.updateText = "Click Start!"
    self.onScreenButtons = self.mainMenuButtons
    self.shownCharacter = self.mainMenuImg
    self.textBox = textBox.TextBox(self.screen)
    self.dialogueMode = False
    self.battleMode = False
    self.script = sp.ScriptParser("Script.txt")
    #self.fightScript = 


  def loop(self):
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
          for b in self.onScreenButtons:
            if b.rect.collidepoint(event.pos):
              b.action()
          if self.dialogueMode:
            #print(self.script.currentLine())
            self.script.next()
          #elif self.battleMode:
            #self.

      if self.battleMode:
        if self.ichigo.health <= 0 or self.aizen.health <= 0:
          print("Hello")
          self.battleMode = False
          self.dialogueMode = True
          del self.onScreenButtons[1:]

        # if self.playerTurn:
        #   pass
        # elif self.enemyTurn:
        #   pass
      elif self.dialogueMode:
        if self.script.currentLine()[0] == "i":
          print("Chingus")
          self.shownCharacter = self.ichigo
        elif self.script.currentLine()[0] == "a":
          self.shownCharacter = self.aizen
        elif self.script.currentLine()[0] == "<BATTLE>": # set up fight buttons
          for b in self.fightButtons:
            self.onScreenButtons.append(b)
          self.battleMode = True
          self.dialogueMode = False
          self.script.next()
        elif self.script.currentLine()[0] == "<END>":
          print("Hello there")
          self.dialogueMode = False
          self.battleMode = False
          self.onScreenButtons = self.mainMenuButtons
          self.shownCharacter = self.mainMenuImg
          self.updateText = "Click Start!"
          self.script.position = -1
      
      #print(self.shownCharacter)
      self.shownCharacter.move()

      self.screen.fill(constants.B_COLOR)
      self.shownCharacter.blit()
      for b in self.onScreenButtons:
        b.blit()
      if self.dialogueMode is True:
        self.textBox.updateText(self.script.currentLine())
      else:
        #print('HELLO')
        self.textBox.updateText(self.updateText)
      self.textBox.blit()
      pygame.display.flip()


  def genItemButtons(self):
    for item in self.ichigo.inventory:
      pass


  def genSkillButtons(self):
    y = 50
    end = []
    for move in self.ichigo.attacks:
      end.append(Button(self.screen, 300, y, self.damageAizen, move.name, arg=move))
      y += 50

    return end


  def skills(self):
    print(self.skillButtons)
    for b in self.skillButtons:
      self.onScreenButtons.append(b)

  def damageAizen(self, atk: Attack):
    c = random.randint(0, 100)

    if c > atk.hitChance:
      self.updateText = atk.name + " missed!"
    else:
      d = random.randint(*atk.dmgRng)
      self.aizen.health -= d

      self.updateText = "Aizen took " + str(d) + " damage!"


  def damageIchigo(self):
    c = random.randint(0, 100)

    if c > atk.hitChance:
      pass


  def changeShownCharacter(self, char):
    self.shownCharacter = char


  def start(self):
    self.dialogueMode = True
    self.onScreenButtons = [self.quitButton]


  def quit(self):   
    sys.exit(23)