import pygame
from KineticButton import KineticButton
from pygame.locals import *
from SaveMenu import SaveMenu
from ConfigMenu import ConfigMenu


class PauseMenu:
    def __init__(self, screen: pygame.Surface, background: pygame.Surface, actual_scene="", actual_screen: pygame.Surface=None):
        self.options = [KineticButton("Reprendre", 10, 20, 200, 30, "resume", background_color=(70, 100, 120), font_size=25, outline=1),
                        KineticButton("Sauvegarder", 10, 60, 200, 30, "save", background_color=(70, 100, 120), font_size=25, outline=1),
                        KineticButton("Charger", 10, 100, 200, 30, "load", background_color=(70, 100, 120), font_size=25, outline=1),
                        KineticButton("Configuration", 10, 140, 200, 30, "config", background_color=(70, 100, 120), font_size=25, outline=1),
                        KineticButton("Menu Principal", 10, 180, 200, 30, "main_menu", background_color=(70, 100, 120), font_size=25, outline=1)]
        self.screen = screen
        self.background = background
        self.actual_screen = actual_screen
        self.actual_scene = actual_scene

        self.hover = -1

    def render(self):
        self.screen.blit(self.background, (0, 0))

        # On assombrit le fond avec un calque
        surface = pygame.Surface((1280, 720))
        surface.fill((0, 0, 0))
        surface.set_alpha(128)

        self.screen.blit(surface, (0, 0))

        for button in self.options:
            button.render(self.screen)

        pygame.display.update()

    def _update_hover_mouse(self, mouse_pos):
        self.options[self.hover].set_is_hover(False)
        is_on_button = False
        for i in range(len(self.options)):
            if self.options[i].do_hover(mouse_pos):
                is_on_button = True
                self.hover = i
        if not is_on_button:
            self.hover = -1
        return is_on_button

    def start(self):
        in_menu = True
        self.render()

        while in_menu:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 'quit'
                if event.type == MOUSEMOTION:
                    if self._update_hover_mouse(pygame.mouse.get_pos()):
                        self.render()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 and self.hover > -1:
                        # Si on clique sur un bouton
                        button_value = self.options[self.hover].get_value()
                        return_val = ""

                        if button_value == 'resume':
                            return ''
                        elif button_value == 'save':
                            menu = SaveMenu(self.screen, self.background, 'save', self.actual_scene, self.actual_screen)
                            return_val = menu.start()
                        elif button_value == 'load':
                            menu = SaveMenu(self.screen, self.background, 'load')
                            return_val = menu.start()
                        elif button_value == 'config':
                            menu = ConfigMenu(self.screen)
                            return_val = menu.start()
                        elif button_value == 'main_menu':
                            return 'main_menu'

                        if return_val == 'quit':
                            return 'quit'
                        if button_value == 'load' and len(return_val) > 0:
                            return ['read', return_val]
                        self.render()
