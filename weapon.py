import pygame
from pygame.locals import *
import sys

class weapon_all:
    def __init__(self):
        self.name = "None"
        self.dmg = 0
        self.rate = 0
        self.x = 0
        self.y = 0


class bullet:
    def __init__(self,x,y):
        self.bullet_img = pygame.image.load("./bullet/handgun1.png")
        self.bullarray = [x,y]

        self.bullarray[0] = x + 80
        self.bullarray[1] = y + 33

        self.width = 50
        self.height = 50

    def bullet_line(self,dire):
        if dire == 1:
            self.bullarray[0] += 10 #玉のスピード.


class magic(weapon_all):
    def __init__(self):
        self.bullet_img = pygame.image.load("./bullet/handgun1.png")
        self.gun_img = pygame.image.load("./weapon/maho.png")
        self.name = "magic"
        self.dmg = 30
        self.rate = 0.5
        self.state = "NOTHING"
        

class handgun(weapon_all):
    def __init__(self):
        self.bullet_img = pygame.image.load("./bullet/handgun1.png")
        self.gun_img = pygame.image.load("./weapon/hg1.png")
        self.name = "handgun"
        self.dmg = 30
        self.rate = 0.5

class ar(weapon_all):
    def __init__(self):
        self.bullet_img = pygame.image.load("./bullet/handgun.png")
        self.gun_img = pygame.image.load("./weapon/ar1.png")
        self.name = "ar"
        self.dmg = 30
        self.rate = 0.5

class smg(weapon_all):
    def __init__(self):
        self.bullet_img = pygame.image.load("./bullet/handgun.png")
        self.gun_img = pygame.image.load("./weapon/smg1.png")
        self.name = "smg"
        self.dmg = 30
        self.rate = 0.5

