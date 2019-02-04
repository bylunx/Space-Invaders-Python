# -*- coding: utf-8 -*-

import sys
import os
import pygame
from random import *
from math import *
from alien import *
import time

LARGEUR = 55
HAUTEUR = 55

class Monster(Alien):

    def __init__(self, fichier_image = "Images/MONSTER.png"):
        Alien.__init__(self, 5, 2, fichier_image)
        self.PV = 1000

    def disparaite(self):
        self.image = pygame.image.load("Images/MONSTER.png").convert()
        self.image.set_alpha(0)

    def apparaitre(self):
        self.image = pygame.image.load("Images/MONSTER.png").convert_alpha()
        self.image.set_alpha(255)

    def update(self):
        self.vitesse_x += 0.05
        pygame.sprite.Sprite.update(self)
        self.mouvement_lateral()
