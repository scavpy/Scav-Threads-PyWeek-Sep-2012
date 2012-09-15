import pygame
from pygame.mixer import Sound, music

import os
import data

VOLUME_LEVEL = 0.5
PHONOGRAPHS = {}
SOUND_ON = True
MUSIC_PLAYING = None

def play(phonograph_name):
    if not SOUND_ON:
        return
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

def orchestrate(phonograph_name, once=False):
    if not SOUND_ON:
        return
    global MUSIC_PLAYING
    if MUSIC_PLAYING == phonograph_name:
        return
    path = data.filepath(
        os.path.join("numerical_phonographs", phonograph_name))
    if MUSIC_PLAYING:
        music.fadeout(1000)
    music.load(path)
    music.play(0 if once else -1)
    MUSIC_PLAYING = phonograph_name
        
def diminuendo(milliseconds):
    if not SOUND_ON:
        return
    music.fadeout(milliseconds)
    global MUSIC_PLAYING
    MUSIC_PLAYING = None
