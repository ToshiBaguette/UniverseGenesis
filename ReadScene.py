import pygame
import io
import TextDisplay
import json
import utils

from pygame.locals import *
from PauseMenu import PauseMenu


class ReadScene:
    def __init__(self, screen: pygame.Surface, scene: str, precedent_music: str = ""):
        self.screen = screen
        self.scene = scene  # On garde le nom de la scène en mémoire pour les sauvegardes
        json_file = io.open("Scenes/scene_" + str(scene) + ".json", 'r', encoding='utf-8')
        json_scene = json.load(json_file)
        json_file.close()

        # La grosse boite de dialogue au milieu de l'écran
        self.scene_text = TextDisplay.TextDisplay(140, 10, 1000, 700, json_scene['text'],
                                                  background_color=(173, 173, 173, 160),
                                                  outline=1, outline_color=(0, 0, 0), text_color=(255, 255, 255),
                                                  font_size=35)
        self.characters = json_scene["personnages"]
        for char in self.characters:
            char["img_loaded"] = pygame.image.load(char["image"])
        self.background = pygame.transform.scale(pygame.image.load("assets/backgrounds/" + json_scene["background"]), (1280, 720))

        self.next_scene = json_scene["next"]
        self.music = json_scene["music"]

        if precedent_music != self.music:
            utils.load_and_play_music(json_scene["music"])

    def render(self):
        self.screen.blit(self.background, (0, 0))
        for char in self.characters:
            self.screen.blit(char["img_loaded"], (char["position"]["x"], char["position"]["y"]))

        self.scene_text.render(self.screen)

        pygame.display.update()

    def start(self):
        in_game = True
        self.render()

        while in_game:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return ['quit', ]
                elif event.type == KEYDOWN:
                    if event.key in [K_RETURN, K_SPACE]:
                        # On passe à la scène d'après
                        return ["read_scene", self.next_scene, self.music]
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
