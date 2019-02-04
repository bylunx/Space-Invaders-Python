# -*- coding: utf-8 -*-

import sys
import os
import pygame
from random import *
from math import *
from ship import *


class Tir(Ship):

    def __init__(self, x, y, tir_ennemi, tir_boss=False, orientation=0):
        pygame.sprite.Sprite.__init__(self)
        Ship.__init__(self)
        self.__image_source = pygame.image.load("Images/tir.png").convert()
        self.image = self.__image_source
        self.sens = None
        self.tir_ennemi = tir_ennemi
        self.tir_boss = tir_boss
        self.tir_x = x
        self.tir_y = y
        self.tir_vitesse_y = 30
        self.orientation = orientation
        self.rect = self.image.get_rect()


    def envoi(self, haut_ou_bas):
        self.rect.topleft = (self.tir_x, self.tir_y)
        if self.tir_boss:
            self.image = pygame.image.load("Images/tir_monster.png").convert_alpha()
        elif self.tir_ennemi:
            self.image = pygame.image.load("Images/tir_enemy.png").convert()

        if haut_ou_bas == True:
            self.tir_vitesse_y = -self.tir_vitesse_y
        elif haut_ou_bas == False:
            self.tir_vitesse_y = self.tir_vitesse_y


    def update(self):
        pygame.sprite.Sprite.update(self)
        if self.orientation != 0:
            self.move = self.rect.move_ip(self.orientation, self.tir_vitesse_y)
        else:
            self.move = self.rect.move_ip(0, self.tir_vitesse_y)
