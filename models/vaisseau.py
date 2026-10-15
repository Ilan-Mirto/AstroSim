import pygame

import constantes as const


class Vaisseau:

    def __init__(self, pos, destinations, couleur, trace=False, sprite=None):
        self.position = pos
        self.destinations = destinations
        self.couleur = couleur
        self.vitesse = 0
        self.derniere_distance = 0
        self.dessine_trajectoire = True
        self.trace = trace
        if sprite:
            try:
                with open(sprite) as sprite_file:
                    raw_sprite = pygame.image.load(sprite_file)
                    self.sprite = pygame.transform.smoothscale(
                        raw_sprite, const.VAISSEAU_TAILLE_SPRITE)
            except Exception:
                self.sprite = None
        else:
            self.sprite = None

    def avance(self, dt):
        x, y = self.position
        destination = self.destinations[0]
        dx, dy = destination.calcule_pos()
        x = (1 - self.vitesse) * x + self.vitesse * dx
        y = (1 - self.vitesse) * y + self.vitesse * dy
        self.position = x, y
        distance = (x-dx)*(x-dx) + (y-dy)*(y-dy)
        if distance > self.derniere_distance:
            self.vitesse += const.VAISSEAU_PAS_VITESSE
        if abs(x-dx) + abs(y-dy) < const.VAISSEAU_TOLERANCE_ARRIVEE:
            if len(self.destinations) > 1:
                self.destinations = self.destinations[1:]
            self.vitesse = 0
        self.derniere_distance = distance

    def dessine(self, s_persistante, s_temp):
        x, y = self.position
        if self.sprite:
            s_temp.blit(self.sprite,
                        (x-const.VAISSEAU_DEMI_TAILLE_SPRITE,
                         y-const.VAISSEAU_DEMI_TAILLE_SPRITE))
        else:
            pygame.draw.rect(
                s_temp, self.couleur,
                (int(x)-const.VAISSEAU_DEMI_TAILLE,
                 int(y)-const.VAISSEAU_DEMI_TAILLE,
                 const.VAISSEAU_TAILLE, const.VAISSEAU_TAILLE))
            pygame.draw.rect(
                s_temp, pygame.Color("white"),
                (int(x)-const.VAISSEAU_DEMI_TAILLE_CENTRE,
                 int(y)-const.VAISSEAU_DEMI_TAILLE_CENTRE,
                 const.VAISSEAU_TAILLE_CENTRE,
                 const.VAISSEAU_TAILLE_CENTRE))
        if self.dessine_trajectoire:
            position = x, y
            for d in self.destinations:
                dx, dy = d.calcule_pos()
                pygame.draw.line(s_temp, self.couleur,
                                 position, (int(dx), int(dy)))
                position = dx, dy
        if self.trace:
            pygame.draw.circle(s_persistante, self.couleur, (int(x), int(y)),
                               const.RAYON_TRACE)
