import pygame
import math

class Planete:

    def __init__(self, taille, rayon_orbite, poids,
                 v_angulaire, couleur, trace=False, phase=0):
        self.taille = taille
        self.rayon_orbite = rayon_orbite
        self.astre_orbite = None

        if astre_orbite is None:
            self.centre_orbite = (1920 / 2, 1080 / 2)
        else:
            self.astre_orbite = astre_orbite
            self.centre_orbite = astre_orbite.calcule_pos()
        
        if isinstance(couleur, pygame.Color):
            self.couleur = couleur
        elif isinstance(couleur, (list, tuple)):
            self.couleur = pygame.Color(*couleur)
        else:
            self.couleur = pygame.Color(couleur)
        self.v_angulaire = v_angulaire
        self.angle = phase
        self.trace = trace

    def calcule_pos(self):
        if self.astre_orbite is not None:
            self.centre_orbite = self.astre_orbite.calcule_pos()
        x = self.centre_orbite[0] + self.rayon_orbite * math.cos(self.angle)
        y = self.centre_orbite[1] + self.rayon_orbite * math.sin(self.angle)
        return x, y

    def dessine(self, s_persistante, s_temp):
        x, y = self.calcule_pos()
        cx, cy = self.centre_orbite
        pygame.draw.circle(s_temp, self.couleur, (int(x), int(y)), self.taille)
        if self.rayon_orbite > 1:
            pygame.draw.circle(s_temp, self.couleur, (int(cx), int(cy)), int(self.rayon_orbite), 1)
        if self.trace:
            pygame.draw.circle(s_persistante, self.couleur, (int(x), int(y)), 1)

    def avance(self, dt):
        self.angle += self.v_angulaire * dt / 10000

