#!/usr/bin/env python3

import math

import pygame

import constantes as const
from models.planete import Planete
import ux_manager as ux
from models.button import Button


class GameEngine:

    from enum import Enum

    class State(Enum):
        PLAY = 0
        PAUSE = 1
        INSPECT_MENU = 2

    def __init__(self):
        self.univers = []
        self.selected_index = None
        self.running = False

        self.state = self.State.PLAY

        self.selected_index = None

    @staticmethod
    def is_quit_event(event):
        return (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE))

    def toggle_menu(self):
        self.menu_is_open = not self.menu_is_open

    def handle_key(self, event):
        if event.key == pygame.K_m and self.state == self.State.PLAY:
            self.state = self.State.INSPECT_MENU
        elif event.key == pygame.K_m and self.state == self.State.INSPECT_MENU:
            self.state = self.State.PLAY

        print(f"DEBUG : state={self.state}, menu_is_open={self.menu_is_open}")

    def handle_click(self, event):
        return

    def handle_events(self):
        for event in pygame.event.get():
            if self.is_quit_event(event):
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_key(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event)


    @staticmethod
    def cree_orbite(centre, masse_etoile, rayon, angle, taille, masse, couleur):
        """Planète en orbite circulaire autour de l'étoile, à l'angle donné."""
        vitesse = math.sqrt(const.CONSTANTE_GRAVITATION * masse_etoile / rayon)
        position = (centre[0] + rayon * math.cos(angle),
                    centre[1] + rayon * math.sin(angle))
        return Planete(taille, vitesse, angle + math.pi / 2, masse, 0, couleur,
                       position_init=position)

    @staticmethod
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

    def run(self):
        interface = ux.UXManager()
        centre = interface.initialize()
        etoile = Planete(const.TAILLE_ETOILE, 0, 0, const.MASSE_ETOILE, 0,
                         const.COULEUR_ETOILE, position_init=centre)
        self.univers = [etoile]
        self.running = True

        while self.running:
            self.handle_events()
            if not self.running:
                break


            interface.render(
                self.univers + const.BUTTONS,
                self.State
            )

            for planet in self.univers:
                for autre in planet.is_touching(self.univers):
                    planet.steal_masse(autre)

            self.univers = [planet for planet in self.univers
                            if planet.masse > 0]

            temps_ecoule = interface.tick(const.FPS) * const.SIMULATION_SPEED
            nouvelles_positions = [
                objet.calcule_pos(self.univers, temps_ecoule)
                for objet in self.univers
            ]
            for objet, position in zip(self.univers, nouvelles_positions):
                objet.position = position

        interface.close()


def main():
    GameEngine().run()


if __name__ == "__main__":
    main()
