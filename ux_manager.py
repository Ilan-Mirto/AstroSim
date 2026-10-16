import constantes as const
import pygame


class UXManager:
    def __init__(self):
        self.ecran = None
        self.surface_persistante = None
        self.surface_temporaire = None
        self.fps_clock = None

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

    def render(self, to_draw, state):
        self.surface_temporaire.fill((0, 0, 0, 0))

        if 

        self.ecran.fill(const.ARRIERE_PLAN)
        self.ecran.blit(self.surface_persistante, (0, 0))
        self.ecran.blit(self.surface_temporaire, (0, 0))
        render_menu(self.ecran, menu_is_open, univers, selected_index)
        buttons = const.MENU_BUTTONS if menu_is_open else []
        for button in buttons:
            button.render(self.ecran)
        pygame.display.update()

    def tick(self, fps):
        return self.fps_clock.tick(fps)

    @staticmethod
    def close():
        pygame.quit()


def render_menu(ecran, menu_is_open, univers, selected_index=None):
    """
    Affiche le menu des informations sur l'univers.
    """
    if not menu_is_open:
        return

    # Dessiner le menu ici
    menu_surface = pygame.Surface((const.MENU_WIDTH, const.MENU_HEIGHT))
    menu_surface.fill((50, 50, 50))  # couleur de fond du menu
    ecran.blit(menu_surface, (0, 0))
    cursor_pos = (0, 0)
    for i in range(len(univers)):
        mouse_inside = _mouse_is_in(
            0, cursor_pos[1], const.MENU_WIDTH, cursor_pos[1] + 40
        )
        if mouse_inside:
            text_color = (255, 255, 0)
        else:
            text_color = (255, 255, 255)
        astre_info = f"Astre n°{i} - Masse: {univers[i].masse}"
        font = pygame.font.Font(None, 36)
        text_surface = font.render(astre_info, True, text_color)
        ecran.blit(text_surface, cursor_pos)
        cursor_pos = (cursor_pos[0], cursor_pos[1] + 40)

    select_font = pygame.font.Font(None, 36)
    selected_text_surface = select_font.render(f"Sélectionné : {selected_index}", True, (255, 0, 0))
    ecran.blit(selected_text_surface, (0, const.MENU_HEIGHT - 40))


def _mouse_is_in(x1, y1, x2, y2):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return x1 <= mouse_x <= x2 and y1 <= mouse_y <= y2
