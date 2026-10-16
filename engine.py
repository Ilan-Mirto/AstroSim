#!/usr/bin/env python3

from modules.camera import Camera

import pygame

import constantes as const
from models.planete import Planete
import ux_manager as ux
from models.button import Button
import math


class GameEngine:

    State = const.State

    def __init__(self):
        self.univers = []
        self.selected_index = None
        self.running = False

        self.state = self.State.PLAY

        self.selected_index = None

        self.ask_question = None
        self.ask_answer = ""
        self.ask_callback = None
        self.placement_pos = None

        self.camera = const.CAMERA

    @staticmethod
    def is_quit_event(event):
        return (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE))

    def handle_key(self, event):
        if self.state == self.State.PLAY:
            if event.key == pygame.K_m and self.selected_index is not None:
                self.state = self.State.INSPECT_MENU

            print("Camera position:", self.camera.get_position())


        elif event.key == pygame.K_m and self.state == self.State.INSPECT_MENU:
            self.state = self.State.PLAY

        elif self.state == self.State.ASK_FOR:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.validate_answer()
            elif event.key == pygame.K_BACKSPACE:
                self.ask_answer = self.ask_answer[:-1]
            elif event.unicode and event.unicode.isprintable():
                self.ask_answer += event.unicode

    def validate_answer(self):
        reponse = self.ask_answer.strip()
        if not reponse:
            return
        callback = self.ask_callback
        self.ask_question = None
        self.ask_answer = ""
        self.ask_callback = None
        self.state = self.State.PLAY
        if callback:
            callback(reponse)

    def place_planet_in_orbit(self, nom):
        """Mémorise le nom puis demande la masse de la nouvelle planète."""
        self.ask_for_str(
            "Masse de la planète : ",
            lambda texte: self.place_planet_with_mass(nom, texte))

    def place_planet_with_mass(self, nom, texte_masse):
        """Crée la planète en orbite autour de l'astre sélectionné,
        à la position choisie pendant l'aperçu."""
        try:
            masse = float(texte_masse.replace(",", "."))
        except ValueError:
            masse = 0
        if not math.isfinite(masse) or masse <= 0:
            self.ask_for_str(
                "Masse invalide (nombre > 0) : ",
                lambda texte: self.place_planet_with_mass(nom, texte))
            return
        if self.selected_index is None or self.selected_index >= len(self.univers):
            return
        astre = self.univers[self.selected_index]
        dx = self.placement_pos[0] - astre.position[0]
        dy = self.placement_pos[1] - astre.position[1]
        distance = max(math.hypot(dx, dy), astre.taille + const.TAILLE_NOUVELLE_PLANETE)
        creation = self.cree_planete if astre is self.univers[0] else self.cree_lune
        planete = creation(
            nom, astre, distance, math.atan2(dy, dx),
            const.TAILLE_NOUVELLE_PLANETE, const.COULEUR_NOUVELLE_PLANETE,
            masse)
        self.univers.append(planete)

    def handle_click(self, event):

        pos = event.pos

        # verification des bouton
        for b in const.BUTTONS:
            if b.is_clicked(pos):
                self.perform_action(b.action)
                return

        if self.state == self.State.PLACE_PREVIEW:
            cam_x, cam_y = self.camera.get_position()
            self.placement_pos = (pos[0] + cam_x, pos[1] + cam_y)
            self.ask_for_str("Nom de la planète : ", self.place_planet_in_orbit)
            return

        if self.state == self.State.PLAY or self.state == self.State.INSPECT_MENU:
            for i, planet in enumerate(self.univers):
                if planet.is_touching_pos(pos):
                    if i == self.selected_index:
                        self.selected_index = None
                        self.state = self.State.PLAY
                        break
                    self.selected_index = i
                    self.state = self.State.INSPECT_MENU
                    break

    def handle_events(self):
        for event in pygame.event.get():
            if self.is_quit_event(event):
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_key(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event)
            self.slide_cam_with_mouse(event)

    def perform_action(self, action):
        if action == "mettre_en_orbite":
            self.state = self.State.PLACE_PREVIEW

    def slide_cam_with_mouse(self, event):
        if event.type == pygame.MOUSEMOTION and (self.state == self.State.PLAY or self.state == self.State.INSPECT_MENU):
            if pygame.mouse.get_pressed()[0]:  # Si le bouton gauche de la souris est enfoncé
                rel = event.rel
                self.camera.move(-rel[0], -rel[1])

    @staticmethod
    def cree_orbite(nom, centre, masse_etoile, rayon, angle, taille, masse, couleur):
        """Planète en orbite circulaire autour de l'étoile, à l'angle donné."""
        vitesse = math.sqrt(const.CONSTANTE_GRAVITATION * masse_etoile / rayon)
        position = (centre[0] + rayon * math.cos(angle),
                    centre[1] + rayon * math.sin(angle))
        return Planete(nom, taille, vitesse, angle + math.pi / 2, masse, 0, couleur,
                       position_init=position)

    @staticmethod
    def cree_planete(nom, etoile, distance, angle, taille, couleur,
                     masse=const.MASSE_LUNE):
        """Planète libre en orbite gravitationnelle circulaire autour de l'étoile."""
        vitesse_relative = math.sqrt(
            const.CONSTANTE_GRAVITATION * etoile.masse / distance)
        vx = (etoile.vitesse * math.cos(etoile.dir)
              + vitesse_relative * math.cos(angle + math.pi / 2))
        vy = (etoile.vitesse * math.sin(etoile.dir)
              + vitesse_relative * math.sin(angle + math.pi / 2))
        position = (etoile.position[0] + distance * math.cos(angle),
                    etoile.position[1] + distance * math.sin(angle))
        return Planete(nom, taille, math.hypot(vx, vy), math.atan2(vy, vx),
                       masse, 0, couleur, position_init=position)

    @staticmethod
    def cree_lune(nom, parent, distance, angle, taille, couleur,
                  masse=const.MASSE_LUNE):
        """Lune dont l'orbite est relative à son parent : elle le suit où qu'il aille."""
        omega = const.OMEGA_LUNE_REFERENCE * (
            const.RAYON_LUNE_REFERENCE / distance) ** 1.5
        lune = Planete(nom, taille, 0, 0, masse, 0, couleur)
        lune.met_en_orbite(parent, distance, angle, omega)
        return lune

    def ask_for_str(self, question, callback):
        self.state = self.State.ASK_FOR
        self.ask_question = question
        self.ask_answer = ""
        self.ask_callback = callback


    def update_simulation(self, dt):
        """Collisions, fusion des masses et déplacement des astres."""
        for planet in self.univers:
            for autre in planet.is_touching(self.univers):
                if autre.parent is planet or planet.parent is autre:
                    continue
                planet.steal_masse(autre)

        self.univers = [planet for planet in self.univers
                        if planet.masse > 0]

        # Un satellite dont le parent a disparu redevient un astre libre
        for planet in self.univers:
            if planet.parent is not None and planet.parent not in self.univers:
                planet.detache()

        libres = [objet for objet in self.univers if objet.parent is None]
        nouvelles_positions = [
            objet.calcule_pos(self.univers, dt) for objet in libres
        ]
        for objet, position in zip(libres, nouvelles_positions):
            objet.position = position

        # Parents avant enfants : l'ordre de création de la liste le garantit
        for objet in self.univers:
            if objet.parent is not None:
                objet.avance_satellite(dt)

    def update(self, dt):
        """Actualise ce qui doit l'être selon l'état courant."""
        if self.state in (self.State.PLAY, self.State.INSPECT_MENU, self.State.PLACE_PREVIEW):
            self.update_simulation(dt)

        if self.state == self.State.ASK_FOR:
            pass

    def run(self):
        interface = ux.UXManager()
        centre = interface.initialize()
        etoile = Planete("Soleil", const.TAILLE_ETOILE, 0, 0, const.MASSE_ETOILE, 0,
                         const.COULEUR_ETOILE, position_init=centre)
        self.univers = [etoile]
        self.running = True
        interface.engine = self

        for button in const.BUTTONS:
            button.engine = self

        while self.running:
            self.handle_events()
            if not self.running:
                break

            interface.render()

            dt = interface.tick(const.FPS) * const.SIMULATION_SPEED
            self.update(dt)

        interface.close()

    def slide_camera(self, dx, dy):
        self.cam_x += dx
        self.cam_y += dy

def main():
    GameEngine().run()


if __name__ == "__main__":
    main()
