import pygame

class Button:
    def __init__(self, label, pos, width, height, action=None, show_state=None, activate=True):
        self.label = label
        self.pos = pos
        self.width = width
        self.height = height
        self.action = action

        self.engine = None

        self.show_state = show_state
        self.activate = activate

    def is_clicked(self, mouse_pos):

        if self.show_state == None or not self.activate:
            return False

        x, y = self.pos
        mx, my = mouse_pos
        return x <= mx <= x + self.width and y <= my <= y + self.height

    def render(self, screen):

        if self.show_state == None or self.show_state != self.engine.state:
            return

        mouse_pos = pygame.mouse.get_pos()

        touched_by_mouse = self.is_clicked(mouse_pos)

        color = (200, 200, 200) if touched_by_mouse else (255, 255, 255)

        x, y = self.pos
        pygame.draw.rect(screen, color, (x, y, self.width, self.height))
        font = pygame.font.Font(None, 36)
        text = font.render(self.label, True, (0, 0, 0))
        text_rect = text.get_rect(center=(x + self.width // 2, y + self.height // 2))
        screen.blit(text, text_rect)