import pygame
import os
import MainMenu
import utils
from ReadScene import ReadScene


def init():
    """Fonction d'initialisation de l'application"""
    # D'abord on vérifie l'existence de tous les répertoires utiles
    repertories = ["scenes", "assets", "saves", "assets/backgrounds", "assets/musics"]
    for rep in repertories:
        if not os.path.isdir(rep):
            os.mkdir(rep)

    # Ensuite on construit notre fenêtre pygame
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((1280, 720))

    cfg = utils.load_settings()
    if cfg["fullscreen"] > 0:
        pygame.display.toggle_fullscreen()

    return screen


def start(screen):
    """Fonction s'occupant rapidement de la boucle de jeu"""
    state = ["main_menu",]
    in_game = True
    while in_game:
        if state[0] == "quit":
            in_game = False
        elif state[0] == "main_menu":
            menu = MainMenu.MainMenu(screen)
            state = menu.start()
        elif state[0] == "read_scene":
            menu = ReadScene(screen, state[1], state[2])
            state = menu.start()


if __name__ == "__main__":
    screen = init()
    start(screen)
    pygame.quit()
