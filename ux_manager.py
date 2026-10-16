import constantes as const
import pygame
import pygame
import math

class UXManager:
    def __init__(self):
        self.ecran = None
        self.surface_persistante = None
        self.surface_temporaire = None
        self.fps_clock = None
        self.engine = None

    def initialize(self):
        pygame.init()
        self.fps_clock = pygame.time.Clock()
        pygame.display.set_caption('Space Oddity')
        info = pygame.display.Info()
        largeur, hauteur = info.current_w, info.current_h
        self.ecran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.surface_persistante = pygame.Surface(
            (largeur, hauteur), pygame.SRCALPHA
        )
        self.surface_temporaire = pygame.Surface(
            (largeur, hauteur), pygame.SRCALPHA
        )
        self.ecran.fill(const.ARRIERE_PLAN)
        return largeur / 2, hauteur / 2

    def render(self):
        State = const.State
        self.surface_temporaire.fill((0, 0, 0, 0))

        if self.engine.state in (State.PLAY, State.INSPECT_MENU, State.PLACE_PREVIEW, State.ASK_FOR):
            self.render_univers(self.surface_persistante, self.surface_temporaire)

        self.ecran.fill(const.ARRIERE_PLAN)
        self.ecran.blit(self.surface_persistante, (0, 0))
        self.ecran.blit(self.surface_temporaire, (0, 0))

        if self.engine.state == State.INSPECT_MENU:
            self.render_menu(self.ecran)

        elif self.engine.state == State.PLACE_PREVIEW:
            self.render_place_preview(self.ecran)

        elif self.engine.state == const.State.ASK_FOR:
            self.render_ask_for(self.ecran)

        for button in const.BUTTONS:
            button.render(self.ecran)

        pygame.display.update()

    def tick(self, fps):
        return self.fps_clock.tick(fps)

    @staticmethod
    def close():
        pygame.quit()
    
    def render_menu(self, ecran):
        """
        Affiche le menu des informations sur l'univers.
        """
        # Dessiner le menu ici
        menu_surface = pygame.Surface((const.MENU_WIDTH, const.MENU_HEIGHT))
        menu_surface.fill((50, 50, 50))  # couleur de fond du menu
        index = self.engine.selected_index
        if index is None or not 0 <= index < len(self.engine.univers):
            ecran.blit(menu_surface, (0, 0))
            return

        astre = self.engine.univers[index]

        font = pygame.font.Font(None, 36)
        text = font.render(astre.nom, True, (255, 255, 255))
        menu_surface.blit(text, (10, 10))
        text = font.render(f"Taille: {astre.taille}", True, (255, 255, 255))
        menu_surface.blit(text, (10, 50))
        text = font.render(f"Masse: {self._int_to_scientific(astre.masse)} T", True, (255, 255, 255))
        menu_surface.blit(text, (10, 90))
        text = font.render(f"Vitesse: {astre.vitesse}", True, (255, 255, 255))
        menu_surface.blit(text, (10, 130))
        text = font.render(f"Direction: {astre.dir}", True, (255, 255, 255))
        menu_surface.blit(text, (10, 170))
        ecran.blit(menu_surface, (0, 0))

        # Affichage de l'élément sélectionné supprimé car selected_index n'est plus passé en paramètre

    def render_univers(self, s_persistante, s_temp):

        univers = self.engine.univers

        for planet in univers:
            planet.render(s_persistante, s_temp)

        # Entourer la planète sélectionnée
        index = self.engine.selected_index
        if index is not None and 0 <= index < len(univers):
            astre = univers[index]

            pos_x = astre.position[0]
            pos_y = astre.position[1]

            pygame.draw.circle(s_temp, (255, 255, 255), (int(pos_x), int(pos_y)), int(astre.taille) + 5, 2)

    def render_place_preview(self, ecran):
        """
        Affiche l'aperçu de placement d'un nouvel astre.
        """
        if self.engine.state != const.State.PLACE_PREVIEW:
            return

        astre_selectionne = self.engine.univers[self.engine.selected_index] if self.engine.selected_index is not None else None

        if astre_selectionne is None:
            self.engine.state = const.State.PLAY
            return

        astre_x = astre_selectionne.position[0]
        astre_y = astre_selectionne.position[1]

        # Dessiner l'aperçu ici (par exemple, un cercle suivant la position de la souris)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.circle(ecran, (200, 200, 200), (mouse_x, mouse_y), 20)
        pygame.draw.circle(ecran, (200, 200, 200), (astre_x, astre_y), int(math.hypot(mouse_x - astre_x, mouse_y - astre_y)), 2)

    def render_ask_for(self, ecran):
        question = self.engine.ask_question
        font = pygame.font.Font(None, 36)
        text = font.render(question, True, (255, 255, 255))
        ecran.blit(text, (10, 10))
        text = font.render(self.engine.ask_answer, True, (255, 255, 255))
        ecran.blit(text, (10, 50))

    @staticmethod
    def _mouse_is_in(x1, y1, x2, y2):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return x1 <= mouse_x <= x2 and y1 <= mouse_y <= y2

    @staticmethod
    def _int_to_scientific(num):
        """
        Convertit un entier en notation scientifique sous forme de chaîne.
        """
        return f"{num:.2e}"
