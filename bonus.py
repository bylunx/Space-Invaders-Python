# -*- coding: utf-8 -*-

import sys
import os
import pygame
from random import *
from math import *
import time


class Bonus(pygame.sprite.Sprite):

    def __init__(self, fichier_image = "Images/bonus.png"):
        pygame.sprite.Sprite.__init__(self)
        self.__image_source = pygame.image.load(fichier_image).convert_alpha()
        self.image = self.__image_source
        self.vitesse_y = 10
        self.rect = self.image.get_rect()
        self.rect.topleft = (randint(0, pygame.display.get_surface().get_width()), 0)

    def mouvement_lateral(self):
        self.rect = self.rect.move(0, self.vitesse_y)

    def update(self):
        pygame.sprite.Sprite.update(self)
        self.vitesse_y += 0.5
        self.mouvement_lateral()
