import io
import json
import pygame
import utils
from pygame.locals import *
from KineticButton import KineticButton
from PauseMenu import PauseMenu


class ReadChoice:
    def __init__(self, screen: pygame.Surface, scene: str, precedent_music: str = ""):
        self.screen = screen
        self.scene = scene  # On garde le nom de la scène en mémoire pour les sauvegardes
        json_file = io.open("Scenes/scene_" + str(scene) + ".json", 'r', encoding='utf-8')
        json_scene = json.load(json_file)
        json_file.close()

        self.choices = []
        i = 0
        for choice in json_scene["choices"]:
            self.choices.append(KineticButton(choice["value"], 340, 100 * i + 5 * i + 100, 500, 40, choice["next"], background_color=(255, 255, 255), text_color=(0, 0, 0)))
            i += 1

        self.characters = json_scene["personnages"]
        for char in self.characters:
            char["img_loaded"] = pygame.image.load(char["image"])

        self.background = pygame.transform.scale(pygame.image.load("assets/backgrounds/" + json_scene["background"]),
                                                 (1280, 720))

        self.music = json_scene["music"]

        if precedent_music != self.music:
            utils.load_and_play_music(json_scene["music"])

        self.hover = 0

    def render(self):
        self.screen.blit(self.background, (0, 0))
        for char in self.characters:
            self.screen.blit(char["img_loaded"], (char["position"]["x"], char["position"]["y"]))

        for choice in self.choices:
            choice.render(self.screen)

        pygame.display.update()

    def _update_hover_keyboard(self, key):
        self.choices[self.hover].set_is_hover(False)

        if key == K_UP:
            if self.hover == 0:
                self.hover = len(self.choices) - 1
            else:
                self.hover -= 1
        elif key == K_DOWN:
            if self.hover == len(self.choices) - 1:
                self.hover = 0
            else:
                self.hover += 1

        self.choices[self.hover].set_is_hover(True)

    def _update_hover_mouse(self, mouse_pos):
        self.choices[self.hover].set_is_hover(False)
        is_on_button = False
        for i in range(len(self.choices)):
            if self.choices[i].do_hover(mouse_pos):
                is_on_button = True
                self.hover = i
        return is_on_button

    def start(self):
        in_game = True
        self.render()

        while in_game:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return ['quit', ]

                elif event.type == MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    self._update_hover_mouse(mouse_pos)
                    self.render()

                elif event.type == KEYDOWN:
                    if event.key in [K_UP, K_DOWN]:
                        self._update_hover_keyboard(event.key)
                        self.render()

                    elif event.key in [K_RETURN, K_SPACE]:
                        val = self.choices[self.hover].get_value()
                        return ['read_scene', val, self.music]

                    elif event.key == K_ESCAPE:
                        # Il va falloir créer et appeler un menu de pause
                        menu = PauseMenu(self.screen, self.background, self.scene, self.screen.copy())
                        action = menu.start()

                        self.render()

                        if action == 'quit':
                            return ['quit', ]
                        elif action == 'main_menu':
                            print("On va vers le main_menu")
                            return ['main_menu', ]
                        elif len(action) > 0 and action[0] == 'read':
                            return ['read_scene', action[1], '']

                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    val = self.choices[self.hover].get_value()
                    return ['read_scene', val, self.music]
