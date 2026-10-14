#! /usr/bin/env python3

import pygame
import sys
import json
from planete import Planete
from vaisseau import Vaisseau

global FPSCLOCK
FPS = 120
WINDOWWIDTH = 1800
WINDOWHEIGHT = 1600
ARRIERE_PLAN = (42,17,51)


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

    etoile = Planete(50, 0, None, 0, (255, 255, 255))
    planete = Planete(30, 150, etoile, 20, (0, 0, 255))
    lune = Planete(10, 50, planete, 40, (200, 200, 200))
    mars = Planete(18, 260, etoile, 12, (220, 90, 50))
    jupiter = Planete(28, 380, etoile, 9, (210, 170, 120))
    saturne = Planete(24, 490, etoile, 7, (230, 210, 150))

    lune2 = Planete(6, 45, saturne, 60, (150, 150, 150))
    lune3 = Planete(7, 35, mars, 80, (180, 180, 180))

    univers = [etoile, planete, lune, mars, jupiter, saturne, lune2, lune3]
    
    ecran.fill(ARRIERE_PLAN)

    while True:  #boucle principale
        try:
            handleEvents()
            drawApp(s_temp, s_pers, ecran, univers)

            temps_ecoule = FPSCLOCK.tick(FPS)
            for objet in univers:
                objet.avance(temps_ecoule)

        except Quitte:
            break
            
    pygame.quit()
    sys.exit(0)

main()
