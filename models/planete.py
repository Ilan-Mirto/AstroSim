import math

import pygame

import constantes as const


from modules.camera import Camera


class Planete:

    def __init__(self, nom, taille, vitesse_init, dir_init, masse,
                 v_angulaire, couleur, trace=True, phase=0,
                 position_init=(0, 0)):

        self.nom = nom

        self.taille = taille
        self.masse = masse
        self.vitesse = vitesse_init
        self.dir = dir_init if dir_init is not None else 0
        self.position = position_init
        self.camera = const.CAMERA
        if isinstance(couleur, pygame.Color):
            self.couleur = couleur
        elif isinstance(couleur, (list, tuple)):
            self.couleur = pygame.Color(*couleur)
        else:
            self.couleur = pygame.Color(couleur)
        self.v_angulaire = v_angulaire
        self.angle = phase
        self.trace = trace
        self.points_trace = []

        # Satellite : orbite calculée relativement à son parent
        self.parent = None
        self.rayon_orbite = 0
        self.angle_orbite = 0
        self.omega = 0

    def met_en_orbite(self, parent, rayon, angle, omega):
        """Fait de cette planète un satellite de `parent` (orbite circulaire)."""
        self.parent = parent
        self.rayon_orbite = rayon
        self.angle_orbite = angle
        self.omega = omega
        self.position = self.position_satellite()
        

    def position_satellite(self):
        return (self.parent.position[0] + self.rayon_orbite * math.cos(self.angle_orbite),
                self.parent.position[1] + self.rayon_orbite * math.sin(self.angle_orbite))

    def avance_satellite(self, dt):
        """Fait tourner le satellite autour de son parent (dt en ms)."""
        self.angle_orbite += self.omega * dt / const.MILLISECONDES_PAR_SECONDE
        self.position = self.position_satellite()

    def detache(self):
        """Libère le satellite avec la vitesse qu'il avait au moment du détachement."""
        v_rel = self.omega * self.rayon_orbite
        tangente = self.angle_orbite + math.pi / 2
        vx = (self.parent.vitesse * math.cos(self.parent.dir)
              + v_rel * math.cos(tangente))
        vy = (self.parent.vitesse * math.sin(self.parent.dir)
              + v_rel * math.sin(tangente))
        self.vitesse = math.hypot(vx, vy)
        self.dir = math.atan2(vy, vx)
        self.parent = None

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
        cam_x, cam_y = self.camera.get_position()
        pygame.draw.circle(s_temp, self.couleur, (int(x) - int(cam_x), int(y) - int(cam_y)), self.taille)
        if self.trace:
            point = (int(x), int(y))
            if not self.points_trace or self.points_trace[-1] != point:
                self.points_trace.append(point)
            largeur, hauteur = s_persistante.get_size()
            marge = const.RAYON_TRACE
            ox, oy = int(cam_x), int(cam_y)
            for px, py in self.points_trace:
                sx, sy = px - ox, py - oy
                if -marge <= sx <= largeur + marge and -marge <= sy <= hauteur + marge:
                    pygame.draw.circle(s_persistante, self.couleur, (sx, sy), marge)

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

    def is_touching_pos(self, pos):
        """Renvoie True si la position donnée touche cette planète."""
        cam_pos = self.camera.get_position()

        x, y = self.position
        dx = pos[0] - x + cam_pos[0]
        dy = pos[1] - y + cam_pos[1]
        distance = math.hypot(dx, dy)
        return distance < self.taille