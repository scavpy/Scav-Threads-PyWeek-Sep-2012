"""
Here the movable typefaces are cast in readiness for use in
publications intended for the edification and instruction of
the operator.
"""

import pygame.font
from pygame.font import Font
import data

STYLE_SIZES = {
    "title":48,
    "subtitle":36,
    "normal":24,
    "small":16,
    }

FONTS = {}

def init():
    pygame.font.init()
    path = data.filepath("Anaktoria.otf")
    for appelation, size in STYLE_SIZES.items():
        FONTS[appelation] = Font(path, size)

init()

def prepare(text, size="normal", colour=(0,0,0)):
    """ prepare a section of text """
    f = FONTS[size]
    return f.render(text, True, colour)

def prepare_title(text, colour=(0,0,0)):
    """ prepare text as a title """
    return prepare(text, size="title", colour=colour)

def prepare_subtitle(text, colour=(0,0,0)):
    """ prepare text as a subtitle """
    return prepare(text, size="subtitle", colour=colour)
