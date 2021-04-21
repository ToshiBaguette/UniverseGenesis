from itertools import chain
import pygame
import os
import io
import json

from datetime import datetime


# PARTIE TEXTE
def truncline(text, font, maxwidth):
    """Fonction coupant le texte en deux pour tenir sur plusieurs lignes à longueur fixe"""
    real = len(text)
    stext = text
    l = font.size(text)[0]
    cut = 0
    a = 0
    done = 1
    while l > maxwidth:
        a = a + 1
        n = text.rsplit(None, a)[0]
        if stext == n:
            cut += 1
            stext = n[:-cut]
        else:
            stext = n
        l = font.size(stext)[0]
        real = len(stext)
        done = 0
    return real, done, stext


def wrapline(text, font, maxwidth):
    """
    Fonction à appeler lorsqu'on veut couper un string en plusieurs lignes (sans prendre les \n en compte)
    :param text: Texte à couper
    :param font: Police de caractère
    :param maxwidth: Taille de la ligne en pixels
    :return: Liste de lignes
    """
    done = 0
    wrapped = []

    while not done:
        nl, done, stext = truncline(text, font, maxwidth)
        wrapped.append(stext.strip())
        text = text[nl:]
    return wrapped


def wrap_multi_line(text, font, maxwidth):
    """
    Fonction à appeler lorsqu'on veut couper un string en plusieurs lignes (prenant en compte les \n)
    :param text: Texte à couper
    :param font: Police de caractères
    :param maxwidth: Taille de la ligne en pixels
    :return: Liste de lignes
    """
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)


# PARTIE MUSIQUE
def load_and_play_music(music):
    cfg = load_settings()
    pygame.mixer.music.load("assets/musics/" + music)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(cfg["sound"] / 100)


# PARTIE OPTIONS
def toggle_fullscreen():
    """Active/Désactive le fullscreen"""
    pygame.display.toggle_fullscreen()


def load_settings():
    """Permet de charger les paramètres"""
    if os.path.isfile("saves/cfg.sav"):
        cfg_file = io.open("saves/cfg.sav", 'r', encoding='utf-8')
        cfg = json.load(cfg_file)
        cfg_file.close()
        return cfg
    else:
        # Ici, on va créer les configs par défaut
        cfg_file = io.open("saves/cfg.sav", 'w', encoding="utf-8")
        cfg_file.write('{"sound":0.5,"fullscreen":0}')
        cfg_file.close()
        return {"sound": 0.5, "fullscreen": 0}


def save_settings(cfg):
    """Permet de sauvegarder les paramètres dans un json"""
    cfg_file = io.open("saves/cfg.sav", 'w', encoding='utf-8')
    cfg_file.write('{"sound":' + str(cfg["sound"]) + ',"fullscreen":' + str(cfg["fullscreen"]) + "}")
    cfg_file.close()


def apply_settings(cfg, fullscreen_changed):
    if fullscreen_changed:
        pygame.display.toggle_fullscreen()
    pygame.mixer.music.set_volume(cfg["sound"])


# PARTIE SAUVEGARDE
def get_saves(page):
    saves = []

    start = page * 16
    for i in range(start, start + 16):
        if os.path.isfile("saves/save" + str(i) + ".jpg") and os.path.isfile("saves/save" + str(i) + ".sav"):
            save_file = io.open("saves/save" + str(i) + ".sav", encoding='utf-8')
            save = json.load(save_file)
            save_file.close()

            saves.append({"image": pygame.transform.scale(pygame.image.load("saves/save" + str(i) + ".jpg"), (256, 144)),
                        "scene": save["scene"], "date": save["date"]})
        else:
            saves.append({"image": None, "scene": None, "date": None})

    return saves


def load_save(nb):
    """Fonction retournant le nom de la scène de la sauvegarde"""
    if os.path.isfile("saves/save" + str(nb) + ".sav"):
        save_file = io.open("saves/save" + str(nb) + ".sav", encoding='utf-8')
        save_state = json.load(save_file)
        save_file.close()
        if save_state["scene"]:
            return save_state["scene"]
    return None


def save(nb, scene, image):
    actual_date = datetime.now()
    date_string = f"{actual_date.day}/{actual_date.month}/{actual_date.year} à {actual_date.hour}:{actual_date.minute}:{actual_date.second}"

    save_file = io.open("saves/save" + str(nb) + ".sav", "w", encoding='utf-8')
    save_file.write('{"scene":"' + str(scene) + '","date":"' + date_string + '"}')
    save_file.close()

    pygame.image.save(image, "saves/save" + str(nb) + ".jpg")

    return None


# PARTIE SCENES
def load_scene(file_path):
    file_scene = io.open("scenes/scene_" + file_path + ".json", 'r', encoding='utf-8')
    json_scene = json.load(file_scene)
    file_scene.close()
    return json_scene

