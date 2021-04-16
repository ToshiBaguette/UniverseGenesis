import pygame


class KineticButton:
    def __init__(self, text: str, x: int, y: int, width: int, height: int, value: str, font="Calibri", font_size=20, text_color=(255, 255, 255), background_color=(0, 0, 0), hover_color=(130, 130, 130), hover=False, outline=0, outline_color=(0, 0, 0), borders=0, border_color=(0, 0, 0)):
        self.text_value = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.value = value
        self.text_color = text_color
        self.background_color = background_color
        self.hover_color = hover_color
        self.outline = outline
        self.outline_color = outline_color
        self.borders = borders
        self.border_color = border_color

        self.font = pygame.font.SysFont(font, font_size)
        self.text_display = self.font.render(self.text_value, False, text_color)
        self.text_outline = self.font.render(self.text_value, False, outline_color)

        self.is_hover = hover

    def set_is_hover(self, n):
        self.is_hover = n

    def do_hover(self, mouse):
        self.is_hover = self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height
        return self.is_hover

    def get_value(self):
        return self.value

    def get_text(self):
        return self.text_value

    def set_text(self, text):
        self.text_value = text
        self.text_display = self.font.render(text, False, self.text_color)
        self.text_outline = self.font.render(text, False, self.outline_color)

    def render(self, screen):
        bg_color = self.background_color
        if self.is_hover:
            bg_color = self.hover_color

        # On va afficher le bouton
        if self.borders > 0:
            screen.fill(self.border_color, (self.x - self.borders, self.y - self.borders, self.width + self.borders * 2, self.height + self.borders * 2))
        screen.fill(bg_color, (self.x,  self.y, self.width, self.height))
        x_text = self.x + self.width // 2 - self.text_display.get_size()[0] // 2
        y_text = self.y + self.height // 2 - self.text_display.get_size()[1] // 2

        # on affiche l'outline
        screen.blit(self.text_outline, (x_text + self.outline, y_text))
        screen.blit(self.text_outline, (x_text - self.outline, y_text))
        screen.blit(self.text_outline, (x_text, y_text + self.outline))
        screen.blit(self.text_outline, (x_text, y_text - self.outline))

        # On affiche enfin le texte normal
        screen.blit(self.text_display, (x_text, y_text))
