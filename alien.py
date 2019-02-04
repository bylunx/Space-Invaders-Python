# -*- coding: utf-8 -*-

import sys
import os
import pygame
from random import *
from math import *
import time

LARGEUR = 55
HAUTEUR = 55

class Alien(pygame.sprite.Sprite):

    def __init__(self, x, y, fichier_image = "Images/alien2.png"):
        pygame.sprite.Sprite.__init__(self)
        self.__image_source = pygame.image.load(fichier_image).convert_alpha()
        self.image = self.__image_source
        self.PV = 100
        self.vitesse_x = 2
        self.rect = self.image.get_rect()
        self.coord_x = x * LARGEUR
        self.coord_y = y * HAUTEUR
        self.rect.topleft = (self.coord_x ,self.coord_y)
        self.__move_block = False
        self.__left_or_right = True
        self.surface = pygame.display.get_surface().get_width()


    def is_out(self):
        if ((self.rect.centerx + 60 > self.surface ) or (self.rect.centerx - 60 < 0 )) and (self.__move_block == False):
            return True
        else:
            return False

    def is_moved(self):
        if self.__move_block == True:
            self.__move_block = not self.__move_block
            return not self.__move_block

    def mouvement_lateral(self):
        if self.__left_or_right == True:
            self.rect = self.rect.move(self.vitesse_x, 0)
        else:
            self.rect = self.rect.move( -self.vitesse_x, 0)


    def mouvement_bas(self):
        self.rect.centery += 20
        self.rect = self.rect.move(-3,0)
        self.__move_block = True
        self.__left_or_right = not self.__left_or_right

    def degat(self):
        self.PV -= 35
        if self.PV <= 0:
            return True

    def affaibli(self):
        self.image = pygame.image.load("Images/alien2_degat.png")

    def disparaite(self):
        self.image = pygame.image.load("Images/alien2_degat.png").convert()
        self.image.set_alpha(0)

    def position_tir_alien(self):
        return [self.rect.centerx, self.rect.centery]

    def apparaitre(self):
        self.image.set_alpha(255)

    def ligne_mire(self, x):
        if (x < self.rect.centerx + 5) and (x > self.rect.centerx - 5):
            return True
        else:
            return False

    def update(self):
        self.vitesse_x += 0.008
        pygame.sprite.Sprite.update(self)
        self.mouvement_lateral()
