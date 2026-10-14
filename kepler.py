#! /usr/bin/env python3

import pygame
import sys
import json
import math
from planete import Planete, CONSTANTE_GRAVITATION
from vaisseau import Vaisseau

global FPSCLOCK
FPS = 120
WINDOWWIDTH = 1800
WINDOWHEIGHT = 1600
ARRIERE_PLAN = (42,17,51)

SIMULATION_SPEED = 1.0


class Quitte(Exception ):
    pass

def isQuitEvent(event):
    return (event.type == pygame.QUIT or 
            (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE))

def handleKey(event):
    print("appui sur la touche", event.key)

def handleClick(event):
    print("Clic à la position", event.pos)

def handleEvents():
    for event in pygame.event.get():
        # pour chaque évènement depuis le dernier appel de cette fonction
        if isQuitEvent(event):
            raise Quitte
        elif event.type == pygame.KEYDOWN:
            handleKey(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("clic")

def drawApp(s_temp, s_pers, ecran, univers):
    """
    Redessine l'écran.
    """
    s_temp.fill((0,0,0,0)) # on remplit avec du transparent
    for objet in univers:
        objet.dessine(s_pers, s_temp)
    ecran.fill(ARRIERE_PLAN)
    ecran.blit(s_pers, (0,0))
    ecran.blit(s_temp, (0,0))
    pygame.display.update()
    
def main():
    temps = 0
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Space Oddity')
    info = pygame.display.Info()
    WINDOWWIDTH, WINDOWHEIGHT = info.current_w,info.current_h
    ecran = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    s_pers = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT), pygame.SRCALPHA)
    s_temp = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT), pygame.SRCALPHA)

    centre = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    masse_etoile = 100000
    vitesse_planete = math.sqrt(CONSTANTE_GRAVITATION * masse_etoile / 150)
    vitesse_mars = math.sqrt(CONSTANTE_GRAVITATION * masse_etoile / 260)
    vitesse_jupiter = math.sqrt(CONSTANTE_GRAVITATION * masse_etoile / 380)
    vitesse_saturne = math.sqrt(CONSTANTE_GRAVITATION * masse_etoile / 490)

    etoile = Planete(50, 0, 0, masse_etoile, 0, (255, 255, 255),
                     position_init=centre)
    planete = Planete(30, vitesse_planete, math.pi / 2, 100, 0,
                      (0, 0, 255), position_init=(centre[0] + 150, centre[1]))
    lune = Planete(10, vitesse_planete + math.sqrt(100 / 50), math.pi / 2,
                   1, 0, (200, 200, 200),
                   position_init=(centre[0] + 200, centre[1]))
    mars = Planete(18, vitesse_mars, math.pi / 2, 15, 0, (220, 90, 50),
                   position_init=(centre[0] + 260, centre[1]))
    jupiter = Planete(28, vitesse_jupiter, math.pi / 2, 300, 0,
                      (210, 170, 120),
                      position_init=(centre[0] + 380, centre[1]))
    saturne = Planete(24, vitesse_saturne, math.pi / 2, 250, 0,
                      (230, 210, 150),
                      position_init=(centre[0] + 490, centre[1]))

    lune2 = Planete(6, vitesse_saturne + math.sqrt(250 / 45), math.pi / 2,
                    1, 0, (150, 150, 150),
                    position_init=(centre[0] + 535, centre[1]))
    lune3 = Planete(7, vitesse_mars + math.sqrt(15 / 35), math.pi / 2,
                    1, 0, (180, 180, 180),
                    position_init=(centre[0] + 295, centre[1]))

    univers = [etoile, planete, lune, mars, jupiter, saturne, lune2, lune3]
    
    ecran.fill(ARRIERE_PLAN)

    while True:  #boucle principale
        try:
            handleEvents()
            drawApp(s_temp, s_pers, ecran, univers)

            temps_ecoule = FPSCLOCK.tick(FPS) * SIMULATION_SPEED
            nouvelles_positions = [
                objet.calcule_pos(univers, temps_ecoule) for objet in univers
            ]
            for objet, position in zip(univers, nouvelles_positions):
                objet.position = position

        except Quitte:
            break
            
    pygame.quit()
    sys.exit(0)

main()
