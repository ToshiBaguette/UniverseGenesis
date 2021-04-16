import pygame
import utils


class TextDisplay:
    def __init__(self, x, y, width, height, text, background_color=(200, 200, 200), text_color=(0, 0, 0), outline=0, outline_color=(0, 0, 0),
                     font="Calibri", font_size=20):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.text = text
        self.background_color = background_color
        self.text_color = text_color
        self.outline = outline
        self.outline_color = outline_color
        self.font = pygame.font.SysFont(font, font_size)

    def render(self, screen):
        # On commence par le background

        bgSurface = pygame.Surface((self.width, self.height))
        alpha = 255
        if len(self.background_color) > 3:
            alpha = self.background_color[3]
        bgSurface.set_alpha(alpha)
        bgSurface.fill(self.background_color)

        screen.blit(bgSurface, (self.x, self.y))

        # On doit construire les strings et les font
        lines = utils.wrap_multi_line(self.text, self.font, self.width)
        display_lines = [self.font.render(txt, False, self.text_color) for txt in lines]
        display_outlines = [self.font.render(txt, False, self.outline_color) for txt in lines]

        # Et finalement on les affiche
        border_y = self.y + self.font.get_height() / 4
        for i in range(len(display_lines)):
            # D'abord les outlines s'il y en a
            if self.outline > 0:
                screen.blit(display_outlines[i], (self.x + 5 - self.outline, border_y))
                screen.blit(display_outlines[i], (self.x + 5 + self.outline, border_y))
                screen.blit(display_outlines[i], (self.x + 5, border_y - self.outline))
                screen.blit(display_outlines[i], (self.x + 5, border_y + self.outline))

            screen.blit(display_lines[i], (self.x + 5, border_y))

            border_y += self.font.get_height() + 10
