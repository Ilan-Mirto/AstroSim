import pygame

class Button:
    def __init__(self, label, pos, width, height, action=None, show=True, activate=True):
        self.label = label
        self.pos = pos
        self.width = width
        self.height = height
        self.action = action

        self.show = show
        self.activate = activate

    def is_clicked(self, mouse_pos):

        if not self.show or not self.activate:
            return False

        x, y = self.pos
        mx, my = mouse_pos
        return x <= mx <= x + self.width and y <= my <= y + self.height

    def render(self, screen):

        if not self.show:
            return

        mouse_pos = pygame.mouse.get_pos()

        touched_by_mouse = self.is_clicked(mouse_pos)

        color = (200, 0, 0) if touched_by_mouse else (255, 0, 0)

        x, y = self.pos
        pygame.draw.rect(screen, color, (x, y, self.width, self.height))
        font = pygame.font.Font(None, 36)
        text = font.render(self.label, True, (255, 255, 255))
        text_rect = text.get_rect(center=(x + self.width // 2, y + self.height // 2))
        screen.blit(text, text_rect)