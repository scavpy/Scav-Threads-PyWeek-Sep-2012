import pygame
from pygame.mixer import Sound

import os
import data

VOLUME_LEVEL = 0.5
PHONOGRAPHS = {}
SOUND_ON = True

def play(phonograph_name):
    if SOUND_ON:
        phonograph = PHONOGRAPHS.get(phonograph_name)
        if not phonograph:
            try:
                phonograph = load_phonograph(phonograph_name)
            except pygame.error:
                print("Missing sound: %s"%phonograph_name)
                return
        phonograph.play()

def load_phonograph(phonograph_name):
    path = data.filepath(
                    os.path.join("numerical_phonographs",phonograph_name))
    phonograph = pygame.mixer.Sound(path)
    phonograph.set_volume(VOLUME_LEVEL)
    PHONOGRAPHS[phonograph_name] = phonograph
    return phonograph

def preload_phonographs(phonographs):
    (load_phonograph(p) for p in phonographs)

def disable_sound():
    global SOUND_ON
    SOUND_ON = False

def enable_sound():
    global SOUND_ON
    SOUND_ON = True
