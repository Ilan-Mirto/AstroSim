#!/usr/bin/env python3

import math
import sys

import pygame

import constantes as const
from models.planete import Planete


class Quitte(Exception):
    pass


def is_quit_event(event):
    return (event.type == pygame.QUIT or
            (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE))


def handle_key(event):
    print("appui sur la touche", event.key)


def handle_click(event):
    print("Clic à la position", event.pos)


def handle_events(univers):
    for event in pygame.event.get():
        # pour chaque évènement depuis le dernier appel de cette fonction
        if is_quit_event(event):
            raise Quitte
        elif event.type == pygame.KEYDOWN:
            handle_key(event)
            if event.key == pygame.K_b:
                univers.append(nouveau_trou_noir(pygame.mouse.get_pos()))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            univers.append(nouvelle_planete(event.pos))


def nouvelle_planete(position):
    from random import randint
    vitesse_init = randint(const.VITESSE_INITIALE_MIN,
                           const.VITESSE_INITIALE_MAX)
    dir_init = math.radians(randint(0, const.DEGRES_PAR_TOUR))
    masse = randint(const.MASSE_INITIALE_MIN, const.MASSE_INITIALE_MAX)
    np = Planete(const.TAILLE_NOUVELLE_PLANETE, vitesse_init, dir_init,
                 masse, 0, const.COULEUR_NOUVELLE_PLANETE,
                 position_init=position, trace=False)
    return np


def nouveau_trou_noir(position):
    """Crée un trou noir à la position donnée."""
    return Planete(const.TAILLE_TROU_NOIR, 0, 0, const.MASSE_TROU_NOIR, 0,
                   const.COULEUR_TROU_NOIR, position_init=position,
                   trace=False)


def draw_app(s_temp, s_pers, ecran, univers):
    """
    Redessine l'écran.
    """
    s_temp.fill((0, 0, 0, 0))  # on remplit avec du transparent
    for objet in univers:
        objet.dessine(s_pers, s_temp)
    ecran.fill(const.ARRIERE_PLAN)
    ecran.blit(s_pers, (0, 0))
    ecran.blit(s_temp, (0, 0))
    pygame.display.update()


def cree_orbite(centre, masse_etoile, rayon, angle, taille, masse, couleur):
    """Planète en orbite circulaire autour de l'étoile, à l'angle donné."""
    vitesse = math.sqrt(const.CONSTANTE_GRAVITATION * masse_etoile / rayon)
    position = (centre[0] + rayon * math.cos(angle),
                centre[1] + rayon * math.sin(angle))
    return Planete(taille, vitesse, angle + math.pi / 2, masse, 0, couleur,
                   position_init=position)


def cree_lune(planete, distance, angle, taille, couleur):
    """Lune en orbite circulaire autour d'une planète."""
    vitesse_relative = math.sqrt(
        const.CONSTANTE_GRAVITATION * planete.masse / distance)
    vx = (planete.vitesse * math.cos(planete.dir)
          + vitesse_relative * math.cos(angle + math.pi / 2))
    vy = (planete.vitesse * math.sin(planete.dir)
          + vitesse_relative * math.sin(angle + math.pi / 2))
    position = (planete.position[0] + distance * math.cos(angle),
                planete.position[1] + distance * math.sin(angle))
    return Planete(taille, math.hypot(vx, vy), math.atan2(vy, vx),
                   const.MASSE_LUNE, 0, couleur, position_init=position)


def main():
    pygame.init()
    fps_clock = pygame.time.Clock()
    pygame.display.set_caption('Space Oddity')
    info = pygame.display.Info()
    window_width, window_height = info.current_w, info.current_h
    ecran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    s_pers = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    s_temp = pygame.Surface((window_width, window_height), pygame.SRCALPHA)

    centre = (window_width / 2, window_height / 2)
    masse_etoile = const.MASSE_ETOILE
    distance_max_ua = max(planete[1] for planete in const.PLANETES_INITIALES)
    echelle_ua = (min(window_width, window_height)
                  * const.FACTEUR_ECHELLE_ORBITALE / distance_max_ua)
    etoile = Planete(const.TAILLE_ETOILE, 0, 0, masse_etoile, 0,
                     const.COULEUR_ETOILE,
                     position_init=centre)

    planetes = []
    for index, (nom, distance_ua, taille, masse, couleur) in enumerate(
            const.PLANETES_INITIALES):
        planete = cree_orbite(
            centre, masse_etoile,
            distance_ua * const.MULTIPLICATEUR_DISTANCE_ORBITALE * echelle_ua,
            index * const.PAS_ANGLE_ORBITAL, taille, masse, couleur)
        planete.nom = nom
        planetes.append(planete)

    univers = [etoile] + planetes

    """ # (rayon, angle, taille, masse, couleur,
    # [(distance lune, angle, taille)])
    nouvelles = [
        (100, 0.6, 12, 20, (160, 160, 170), []),
        (190, 1.3, 16, 40, (240, 200, 90), [(28, 0.5, 4)]),
        (230, 2.0, 20, 60, (90, 200, 120), [(32, 1.0, 5), (45, 3.5, 4)]),
        (330, 2.7, 22, 80, (200, 80, 160), []),
        (420, 3.4, 26, 200, (120, 160, 255), [(40, 2.0, 5)]),
        (520, 4.0, 22, 150, (255, 140, 60), [(36, 0.2, 4), (50, 4.0, 5)]),
        (600, 4.7, 18, 50, (140, 255, 230), []),
        (680, 5.3, 24, 120, (255, 100, 100), [(38, 2.5, 5)]),
        (760, 5.9, 20, 70, (180, 130, 255), [(34, 1.5, 4), (46, 5.0, 4)]),
        (840, 0.3, 16, 30, (220, 220, 100), [(30, 3.0, 4)]),
    ]
    for rayon, angle, taille, masse, couleur, lunes in nouvelles:
        corps = cree_orbite(centre, masse_etoile, rayon, angle, taille,
                            masse, couleur)
        univers.append(corps)
        for distance, angle_lune, taille_lune in lunes:
            univers.append(cree_lune(corps, distance, angle_lune,
                                     taille_lune, (190, 190, 190)))"""

    ecran.fill(const.ARRIERE_PLAN)

    while True:  # boucle principale
        try:
            handle_events(univers)
            draw_app(s_temp, s_pers, ecran, univers)

            for planet in univers:
                for autre in planet.is_touching(univers):
                    planet.steal_masse(autre)

                if planet.masse <= 0:
                    univers.remove(planet)

            temps_ecoule = fps_clock.tick(const.FPS) * const.SIMULATION_SPEED
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
