# -*- coding: utf-8 -*-

import sys
import os
import pygame
from random import *
from math import *


LARGEUR = 55
HAUTEUR = 55

class Ship(pygame.sprite.Sprite):

    def __init__(self, ship_image = "Images/ship1.png"):
        pygame.sprite.Sprite.__init__(self)
        self.__image_source = pygame.image.load(ship_image).convert_alpha()
        self.image = self.__image_source
        self.PV = 100
        self.vitesse_x = 30
        self.rect = self.image.get_rect()
        self.surface_largeur = pygame.display.get_surface().get_width()
        self.surface_hauteur = pygame.display.get_surface().get_height()
        self.rect.topleft = (((self.surface_largeur / 2) - 50), self.surface_hauteur - 140)

    def update(self):
        pygame.sprite.Sprite.update(self)

    def degat(self):
        self.PV -= 25
        if self.PV <= 0:
            return True

    def deplacement_gauche(self):
        if not (self.rect.centerx - 70 < 0):
            self.rect = self.rect.move(-self.vitesse_x, 0)

    def deplacement_droite(self):
        if not (self.rect.centerx + 70 > self.surface_largeur):
            self.rect = self.rect.move(self.vitesse_x, 0)

    def position_tir(self):
        return [self.rect.centerx, self.rect.centery]

    def affichage_PV(self):
        if self.PV == 100:
            return 0
        elif self.PV == 75:
            return 25
        elif self.PV == 50:
            return 50
        elif self.PV == 25:
            return 75
        elif self.PV == 0:
            return 100
        else:
            return 100

    def disparait(self):
        self.image = pygame.image.load("Images/ship1.png").convert()
        self.image.set_alpha(0)

    def apparait(self):
        self.image = pygame.image.load("Images/ship1.png").convert_alpha()
        self.image.set_alpha(255)

    def mort(self):
        self.PV = 0
