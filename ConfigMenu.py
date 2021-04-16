import pygame
import utils
from KineticButton import KineticButton
from pygame.locals import *


class ConfigMenu:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        self.options = [
            KineticButton("<", 15, 15, 40, 40, "back", "Calibri", 30, background_color=(70, 100, 120), hover_color=(240, 230, 50), borders=2),
            KineticButton("Activé", 200, 200, 150, 30, "toggle_fullscreen", "Calibri", 30, background_color=(70, 100, 120),
                          hover_color=(240, 230, 50), borders=2),
            KineticButton("Appliquer", 20, 300, 130, 30, "apply", 'Calibri', 30, background_color=(70, 100, 120),
                          hover_color=(240, 230, 50), borders=2)
        ]
        self.hover = -1

        self.config = utils.load_settings()
        self._update_button()
        self.actual_fullscreen = self.config["fullscreen"]

        self.volume_x = self.config["sound"] * 500 + 200
        self.click_volume = False
        self.offset_click = 0

    def render(self):
        self.screen.fill((70, 100, 120))

        font = pygame.font.SysFont("Calibri", 25)
        fullscreen_text = font.render("Plein écran :", False, (255, 255, 255))
        volume_text = font.render("Volume :", False, (255, 255, 255))

        self.screen.blit(fullscreen_text, (5, 200))
        self.screen.blit(volume_text, (5, 100))

        for button in self.options:
            button.render(self.screen)

        # Barre de volume
        self.screen.fill((255, 255, 255), (200, 107, 500, 5))
        pygame.draw.ellipse(self.screen, (255, 255, 255), (self.volume_x + 200, 100, 20, 20))

        pygame.display.update()

    def _update_hover(self, mouse_pos):
        do_hover = False
        for i in range(len(self.options)):
            if self.options[i].do_hover(mouse_pos):
                do_hover = True
                self.hover = i
        if not do_hover:
            self.hover = -1

    def _update_button(self):
        # On modifie la valeur du bouton toggle_fullscreen en fonction de la config actuelle
        if self.config["fullscreen"] == 1:
            self.options[1].set_text("Activé")
        else:
            self.options[1].set_text("Désactivé")

    def _on_volume(self, mouse_pos):
        return 200 <= mouse_pos[0] <= 700 and 100 <= mouse_pos[1] <= 120

    def start(self):
        in_menu = True

        self.render()
        while in_menu:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 'quit'

                elif event.type == MOUSEMOTION:
                    self._update_hover(pygame.mouse.get_pos())

                    if self.click_volume:
                        self.volume_x = pygame.mouse.get_pos()[0] + self.offset_click
                        if self.volume_x < 0:
                            self.volume_x = 0
                        elif self.volume_x > 500:
                            self.volume_x = 500
                        self.config["sound"] = (self.volume_x - 200) / 500

                    self.render()

                elif event.type == MOUSEBUTTONDOWN:
                    if self.hover > -1:
                        val = self.options[self.hover].get_value()
                        if val == 'back':
                            return ''
                        elif val == 'toggle_fullscreen':
                            self.config["fullscreen"] = (self.config["fullscreen"] + 1) % 2
                            self._update_button()
                            self.render()
                        elif val == 'apply':
                            utils.save_settings(self.config)
                            utils.apply_settings(self.config, self.actual_fullscreen != self.config["fullscreen"])
                            self.actual_fullscreen = self.config["fullscreen"]
                            self.render()
                    elif self._on_volume(pygame.mouse.get_pos()) and event.button == 1:
                        self.click_volume = True
                        self.offset_click = self.volume_x - pygame.mouse.get_pos()[0]

                elif event.type == MOUSEBUTTONUP and event.button == 1:
                    self.click_volume = False
