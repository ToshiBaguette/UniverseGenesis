import pygame
import utils

from pygame.locals import *
from KineticButton import KineticButton


class SaveMenu:
    def __init__(self, screen: pygame.Surface, background: pygame.Surface, action: str, actual_scene="", actual_screen: pygame.Surface=None):
        self.screen = screen
        self.background = background
        self.action = action
        self.actual_screen = actual_screen
        self.actual_scene = actual_scene

        self.page = 0
        self.saves = utils.get_saves(0)
        self.hover = -1
        self.button_hover = -1

        self.buttons = [
            # D'abord le bouton back
            KineticButton("<", 15, 15, 40, 40, "back", "Calibri", 30, background_color=(70, 100, 120), hover_color=(240, 230, 50))
        ]
        # Maintenant les boutons pour les pages
        for i in range(26):
            x_range = i % 2
            y_range = i // 2
            self.buttons.append(KineticButton(str(i + 1), x_range * 45 + 1185, y_range * 45, 40, 40, str(i), "Calibri", 30, background_color=(70, 100, 120), hover_color=(240, 230, 50)))

    def render(self):
        self.screen.blit(self.background, (0, 0))

        # On assombrit le fond avec un calque
        surface = pygame.Surface((1280, 720))
        surface.fill((0, 0, 0))
        surface.set_alpha(128)

        self.screen.blit(surface, (0, 0))

        # On affiche toutes les saves
        offset_x = 132
        for y in range(4):
            for x in range(4):
                index = (y * 4 + x)
                color_back = (70, 100, 120)
                if index == self.hover:
                    color_back = (240, 230, 50)
                self.screen.fill(color_back, (x * 259 + 5 * x + offset_x, y * 147 + y * 5, 259, 147))
                if self.saves[index]["image"]:
                    self.screen.blit(self.saves[index]["image"], (x * 259 + 5 * x + 2 + offset_x, y * 147 + 5 * y + 2))

        back_button_color = (70, 100, 120)

        if self.hover > -1:
            # Menu en bas permettant d'afficher les infos de la save
            self.screen.fill((70, 100, 120), (10, 608, 1260, 115))

            text_scene = "Scene: "
            text_date = "Date: "
            if self.saves[self.hover]["scene"]:
                text_scene += self.saves[self.hover]["scene"]
            else:
                text_scene += "---"

            if self.saves[self.hover]["date"]:
                text_date += self.saves[self.hover]["date"]
            else:
                text_date += "---"

            font = pygame.font.SysFont("Calibri", 25)
            display_scene = font.render(text_scene, False, (255, 255, 255))
            display_date = font.render(text_date, False, (255, 255, 255))
            self.screen.blit(display_date, (15, 613))
            self.screen.blit(display_scene, (15, 650))

        for button in self.buttons:
            button.render(self.screen)

        pygame.display.update()

    def _update_hover(self, mouse_pos):
        on_save = False
        offset_x = 132
        for y in range(4):
            for x in range(4):
                index = (y * 4 + x)
                if x * 257 + 5 * x + offset_x < mouse_pos[0] < x * 257 + 5 + 258 + offset_x and y * 145 + y * 5 < mouse_pos[1] < y * 145 + y * 5 + 145:
                    self.hover = index
                    on_save = True
        if not on_save:
            self.hover = -1
            on_button = False
            for i in range(len(self.buttons)):
                if self.buttons[i].do_hover(mouse_pos):
                    self.button_hover = i
                    on_button = True
            if not on_button:
                self.button_hover = -1

    def start(self):
        in_menu = True

        self.render()
        while in_menu:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 'quit'
                if event.type == MOUSEMOTION:
                    self._update_hover(pygame.mouse.get_pos())
                    self.render()
                if event.type == MOUSEBUTTONDOWN:
                    if self.button_hover > -1:
                        if self.buttons[self.button_hover].get_value() == "back":
                            return ''  # Bouton retour

                        else:
                            # Dans ce cas, on a cliqué sur un bouton pour changer de page
                            self.page = int(self.buttons[self.button_hover].get_value())
                            self.saves = utils.get_saves(self.page)
                            self.render()
                    elif self.hover > -1 and self.saves[self.hover]:
                        if self.action == 'save':
                            utils.save(self.hover + self.page * 16, self.actual_scene, self.actual_screen)
                            self.saves = utils.get_saves(self.page)
                            self.render()
                        else:
                            return utils.load_save(self.hover + self.page * 16)
