import pygame
import math

CONSTANTE_GRAVITATION = 1.1

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
            facteur = CONSTANTE_GRAVITATION * autre.masse / (
                distance_carree * math.sqrt(distance_carree)
            )
            acceleration_x += dx * facteur
            acceleration_y += dy * facteur

        dt_secondes = dt / 1000
        vitesse_x = self.vitesse * math.cos(self.dir) + acceleration_x * dt_secondes
        vitesse_y = self.vitesse * math.sin(self.dir) + acceleration_y * dt_secondes
        self.vitesse = math.hypot(vitesse_x, vitesse_y)
        self.dir = math.atan2(vitesse_y, vitesse_x)
        return x + vitesse_x * dt_secondes, y + vitesse_y * dt_secondes

    def dessine(self, s_persistante, s_temp):
        x, y = self.calcule_pos()
        pygame.draw.circle(s_temp, self.couleur, (int(x), int(y)), self.taille)
        if self.trace:
            pygame.draw.circle(s_persistante, self.couleur, (int(x), int(y)), 1)

    def avance(self, dt, liste_planetes=None):
        self.position = self.calcule_pos(liste_planetes or [self], dt)

