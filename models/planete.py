import math

import pygame

import constantes as const


class Planete:

    def __init__(self, taille, vitesse_init, dir_init, masse,
                 v_angulaire, couleur, trace=True, phase=0,
                 position_init=(0, 0)):
        self.taille = taille
        self.masse = masse
        self.vitesse = vitesse_init
        self.dir = dir_init if dir_init is not None else 0
        self.position = position_init

        if isinstance(couleur, pygame.Color):
            self.couleur = couleur
        elif isinstance(couleur, (list, tuple)):
            self.couleur = pygame.Color(*couleur)
        else:
            self.couleur = pygame.Color(couleur)
        self.v_angulaire = v_angulaire
        self.angle = phase
        self.trace = trace

    def calcule_pos(self, liste_planetes=None, dt=0):
        if not liste_planetes or dt <= 0:
            return self.position

        x, y = self.position
        acceleration_x = 0
        acceleration_y = 0
        for autre in liste_planetes:
            if autre is self or autre.masse <= 0:
                continue
            dx = autre.position[0] - x
            dy = autre.position[1] - y
            distance_carree = dx * dx + dy * dy
            if distance_carree == 0:
                continue
            facteur = const.CONSTANTE_GRAVITATION * autre.masse / (
                distance_carree * math.sqrt(distance_carree)
            )
            acceleration_x += dx * facteur
            acceleration_y += dy * facteur

            if acceleration_x == 0 and acceleration_y == 0:
                continue

            # ? limiter la vitesse maximale
            if acceleration_x > const.ACCELERATION_MAXIMALE:
                acceleration_x = const.ACCELERATION_MAXIMALE
            elif acceleration_x < -const.ACCELERATION_MAXIMALE:
                acceleration_x = -const.ACCELERATION_MAXIMALE
            if acceleration_y > const.ACCELERATION_MAXIMALE:
                acceleration_y = const.ACCELERATION_MAXIMALE
            elif acceleration_y < -const.ACCELERATION_MAXIMALE:
                acceleration_y = -const.ACCELERATION_MAXIMALE

        dt_secondes = dt / const.MILLISECONDES_PAR_SECONDE
        vitesse_x = self.vitesse * \
            math.cos(self.dir) + acceleration_x * dt_secondes
        vitesse_y = self.vitesse * \
            math.sin(self.dir) + acceleration_y * dt_secondes
        self.vitesse = math.hypot(vitesse_x, vitesse_y)
        self.dir = math.atan2(vitesse_y, vitesse_x)
        return x + vitesse_x * dt_secondes, y + vitesse_y * dt_secondes

    def render(self, s_persistante, s_temp):
        x, y = self.calcule_pos()
        pygame.draw.circle(s_temp, self.couleur, (int(x), int(y)), self.taille)
        if self.trace:
            pygame.draw.circle(s_persistante, self.couleur, (int(x), int(y)),
                               const.RAYON_TRACE)

    def avance(self, dt, liste_planetes=None):
        self.position = self.calcule_pos(liste_planetes or [self], dt)

    def is_touching(self, liste_planetes):
        """Renvoie la liste des planètes qui touchent cette planète."""
        x, y = self.position
        res = []
        for autre in liste_planetes:
            if autre is self:
                continue
            dx = autre.position[0] - x
            dy = autre.position[1] - y
            distance = math.hypot(dx, dy)
            if distance < self.taille + autre.taille:
                res.append(autre)
        return res

    def steal_masse(self, autre):
        """Voler la masse d'une autre planète si elles se touchent."""
        if len(autre.is_touching([self])) > 0:
            if self.masse >= autre.masse:
                self.masse += const.MASSE_TRANSFEREE_PAR_COLLISION
                autre.masse -= const.MASSE_TRANSFEREE_PAR_COLLISION

    def is_hitting(self, pos):
        """Renvoie True si la position donnée touche cette planète."""
        x, y = self.position
        dx = pos[0] - x
        dy = pos[1] - y
        distance = math.hypot(dx, dy)
        return distance < self.taille