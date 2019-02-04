#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import pygame
from random import *
from alien import *
from ship import *
from bonus import *
from monster import *
from tir import *
from pygame.locals import *
import time

#---------------------DELETE SPRITE---------------------------------------------------------


def delete_sprite(groupe):
    for index, sprite in enumerate(groupe):
        if index < 10:
            groupe.remove(sprite)
            sprite.kill()

#---------------------GENERATEUR ALIEN---------------------------------------------------------

def generateur_alien():
    nbre_rangee = range(1,4)
    groupe = pygame.sprite.Group()

    for a in nbre_rangee:
        for i in range(1,13):
            groupe.add(Alien(i,a))

    return groupe

#---------------------MAIN---------------------------------------------------------


def main():
    pygame.init()
    size = width, height =  1024, 768
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)#,pygame.FULLSCREEN)

    #Titre
    pygame.display.set_caption("Aliens Invasion")

    #Chargement et collage du fond
    fond = pygame.image.load("Images/fond.jpg").convert()
    fond = pygame.transform.scale(fond,size)

    menu = pygame.image.load("Images/menu.png").convert()
    menu = pygame.transform.scale(menu,size)


    ship = Ship()
    groupe_ship = pygame.sprite.Group()
    groupe_ship.add(ship)

    groupe_alien = generateur_alien()

    groupe_boss = pygame.sprite.Group()

    groupe_tir = pygame.sprite.Group()
    groupe_tir_alien = pygame.sprite.Group()

    groupe_tir_monster = pygame.sprite.Group()

    groupe_bonus = pygame.sprite.Group()

    liste_tir_alien = []
    liste_tir_monster=[]
    liste_tir = []

    dico_duree = {}

    temps_bonus = time.time() + randint(5, 25)

    bonus_active = boss_fin = partie_terminee = perdu = False


    BLOQUANT_monster = BLOQUANT = menu_bloquant = BLOQUANT_spawn = BLOQUANT_bonus = True

    ship_clig = time_bloquant = time_bloquant_monster = time_active = debut = boss_time = 0


    clock = pygame.time.Clock()


#---------------------BOUCLE 1---------------------------------------------------------


    while menu_bloquant:
        screen.blit(menu, (0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            # Une touche est appuyée

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    menu_bloquant = False


#---------------------BOUCLE 2---------------------------------------------------------

    while 1:
        clock.tick(15)
        for event in pygame.event.get():
            # Une touche est appuyée

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                        sys.exit()

                elif event.key == pygame.K_RETURN:
                    if partie_terminee:
                        ship = Ship()
                        groupe_ship = pygame.sprite.Group()
                        groupe_ship.add(ship)

                        groupe_alien = generateur_alien()
                        groupe_boss = pygame.sprite.Group()
                        groupe_bonus = pygame.sprite.Group()

                        groupe_tir = pygame.sprite.Group()
                        groupe_tir_alien = pygame.sprite.Group()

                        liste_tir_alien = []
                        liste_tir_monster=[]
                        liste_tir = []
                        dico_duree = {}

                        temps_bonus = time.time() + randint(5, 25)

                        BLOQUANT = BLOQUANT_spawn = BLOQUANT_bonus = True
                        time_bloquant_monster = time_bloquant = ship_clig = 0

                        partie_terminee = perdu = BLOQUANT_monster = boss_fin = False


                if event.key == pygame.K_UP:
                    if not partie_terminee:
                        if (time.time() - debut) > 0.5:
                            debut = time.time()
                            pos_ship = ship.position_tir()
                            tir = Tir(pos_ship[0], pos_ship[1], False) #position x et y du vaisseau
                            tir.envoi(True)
                            groupe_tir.add(tir)
                            liste_tir.append(tir)
                            if bonus_active:
                                tir1 = Tir(pos_ship[0], pos_ship[1], False, False, 10) #position x et y du vaisseau
                                tir2 = Tir(pos_ship[0], pos_ship[1], False, False, -10) #position x et y du vaisseau
                                tir1.envoi(True)
                                tir2.envoi(True)
                                groupe_tir.add(tir1,tir2)
                                liste_tir.extend((tir1, tir2))



#---------------------TIR ENNEMI---------------------------------------------------------

        for alien in groupe_alien:
            if (pygame.sprite.collide_rect(alien, ship)):
                ship.mort()

            pos_vaisseau = ship.position_tir()

            if alien.ligne_mire(pos_vaisseau[0]) and BLOQUANT and not partie_terminee:
                pos_alien = alien.position_tir_alien()
                tir = Tir(pos_alien[0], pos_alien[1], True)
                tir.envoi(False)
                groupe_tir_alien.add(tir)
                liste_tir_alien.append(tir)
                BLOQUANT = False
                time_bloquant = time.time()

        if time.time() - time_bloquant > 1:
            BLOQUANT = True

#---------------------TIR BOSS MONSTER---------------------------------------------------------

        if boss_fin:
            if ((BLOQUANT_monster) and (not partie_terminee)) :
                pos_monster = monster.position_tir_alien()
                tir = Tir(pos_monster[0] - 180, pos_monster[1], True, True)
                tir2 = Tir(pos_monster[0] - 180, pos_monster[1], True, True, 20)
                tir3 = Tir(pos_monster[0] - 180, pos_monster[1], True, True, -20)
                tir.envoi(False)
                tir2.envoi(False)
                tir3.envoi(False)
                groupe_tir_alien.add(tir)
                liste_tir_alien.append(tir)
                groupe_tir_alien.add(tir,tir2,tir3)
                liste_tir_alien.extend((tir, tir2, tir3))
                time_bloquant_monster = time.time()
                BLOQUANT_monster = False

            if time.time() - time_bloquant_monster > 2.5:
                BLOQUANT_monster = True


#---------------------VAISSEAU BLESSE---------------------------------------------------------

        for tir in liste_tir_alien:
            if (pygame.sprite.collide_rect(tir, ship)):
                tir.remove(groupe_tir)
                liste_tir_alien.remove(tir)
                tir.kill()
                ship.disparait()
                ship.degat()
                ship_clig = time.time()

        if (time.time() - ship_clig) > 0.05:
            ship.apparait()

#---------------------DEPLACEMENT DU VAISSEAU---------------------------------------------------------
        if pygame.key.get_pressed()[K_LEFT]:
            ship.deplacement_gauche()

        elif pygame.key.get_pressed()[K_RIGHT]:
            ship.deplacement_droite()

#---------------------DEPLACEMENT ALIEN SORTI DE MAP---------------------------------------------------------
        if not boss_fin:
            for alien in groupe_alien:
                if not alien.is_moved() and alien.is_out():
                    for alien in groupe_alien:
                        alien.mouvement_bas()
                    break
        else:
            if not monster.is_moved() and monster.is_out():
                monster.mouvement_bas()



#---------------------COLLISION TIR ALIEN---------------------------------------------------------
        if len(groupe_alien) == 0:
            groupe_cible = groupe_boss
        else:
            groupe_cible = groupe_alien

        for shoot in groupe_tir:
            for ennemi in groupe_cible:
                if (pygame.sprite.collide_rect(shoot, ennemi)):
                    if ((len(groupe_alien) < 3) and (groupe_cible == groupe_alien)):
                        ennemi.kill()
                    shoot.remove(groupe_tir)
                    ennemi.disparaite()

                    if groupe_cible == groupe_boss:
                        boss_time = time.time()
                    else:
                        dico_duree[ennemi] = time.time()

                    if ennemi.degat():
                        ennemi.remove(groupe_cible)

#---------------------ALIEN BLESSE ---------------------------------------------------------
        if len(groupe_alien) == 0:
            if (time.time() - boss_time) > 0.05:
                try:
                    monster.apparaitre()
                    objet_touche = monster
                except:
                    pass

        else:
            for ennemi, temps in dico_duree.iteritems():
                if (time.time() - temps) > 0.05:
                    ennemi.affaibli()
                    ennemi.apparaitre()
                    objet_touche = ennemi

        try:
            del dico_duree[objet_touche] # Vidage automatique du dictionnaire pour eviter l'usage inutile de la memoire
        except:
            pass

#---------------------ACTUALISATION---------------------------------------------------------
        groupe_alien.update()
        groupe_alien.draw(screen)

        groupe_ship.update()
        groupe_ship.draw(screen)

        groupe_tir.update()
        groupe_tir.draw(screen)

        groupe_tir_alien.update()
        groupe_tir_alien.draw(screen)

        groupe_bonus.update()
        groupe_bonus.draw(screen)

        groupe_boss.update()
        groupe_boss.draw(screen)

#---------------------GESTION BONUS---------------------------------------------------------


        if (time.time() > temps_bonus) and (BLOQUANT_bonus):
            bonus = Bonus()
            groupe_bonus.add(bonus)
            temps_bonus = temps_bonus + 20

        for bonus in groupe_bonus:
            if pygame.sprite.collide_rect(bonus, ship):
                bonus_active = True
                time_active = time.time()
                groupe_bonus.remove(bonus)
                bonus.kill()

        if (time.time() - time_active) > 7:
            bonus_active = False


#---------------------AFFICHAGE POLICE---------------------------------------------------------

        myfont = pygame.font.SysFont("monospace", 60)
        myfont2 = pygame.font.SysFont("monospace", 40)

        if len(groupe_alien) == 0:
            if BLOQUANT_spawn:
                boss_fin = True
                monster = Monster()
                groupe_boss.add(monster)
                BLOQUANT_spawn = False
            if (len(groupe_boss) == 0) and (not perdu):
                label = myfont.render(u"Vous avez gagné !", 1, (0,255,0))
                label2 = myfont2.render(u"Appuyez sur Entrée pour recommencer", 1, (255,255,255))
                screen.blit(label, (250, 250))
                screen.blit(label2, (100, 300))
                partie_terminee = True
                bonus_active = False
                boss_fin = False
                bonus_active = False
                BLOQUANT_bonus = False
                try:
                    groupe_boss.remove(monster)
                    monster.kill()
                except:
                    pass

        image_PV = pygame.image.load("Images/PV.png").convert()
        screen.blit(image_PV,(width/1.25, 12))

        pygame.draw.rect(fond, (255,0,0), pygame.Rect((width/1.2), 22, 100, 10))

#---------------------PARTIE TERMINEE---------------------------------------------------------

        PV_ship = (ship.affichage_PV())

        if PV_ship == 100:
            pygame.draw.rect(fond, (0,0,0), pygame.Rect((width/1.2), 22, PV_ship, 10))
            label = myfont.render(u"GAME OVER", 1, (255,0,0))
            label2 = myfont2.render(u"Appuyez sur Entrée pour recommencer", 1, (255,255,255))
            screen.blit(label, (350, 250))
            screen.blit(label2, (100, 300))
            partie_terminee = True
            bonus_active = False
            BLOQUANT_bonus = False
            ship.kill()
            try:
                perdu = True
                groupe_boss.remove(monster)
            except:
                pass

        elif not partie_terminee:
            pygame.draw.rect(fond, (0,0,0), pygame.Rect((width/1.2), 22, PV_ship, 10))

        pygame.draw.rect(fond, (255,255,255), pygame.Rect((width/1.2), 22, 100, 10), 1)

#---------------------FIN---------------------------------------------------------

        # Actualisation de l'écran
        pygame.display.flip()

        screen.blit(fond, (0,0))

if __name__ == '__main__':
    main()
