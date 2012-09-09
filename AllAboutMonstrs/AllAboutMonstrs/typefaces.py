"""
Here the movable typefaces are cast in readiness for use in
publications intended for the edification and instruction of
the operator.
"""

import pygame.font
from pygame.font import Font
import data

TITLE_SIZE = 48
SUBTITLE_SIZE = 36
NORMAL_SIZE = 24
SMALL_SIZE = 16

TYPEFACE_PATH = data.filepath("Anaktoria.otf")

pygame.font.init()
TITLE = Font(TYPEFACE_PATH, TITLE_SIZE)
SUBTITLE = Font(TYPEFACE_PATH, SUBTITLE_SIZE)
NORMAL = Font(TYPEFACE_PATH, NORMAL_SIZE)
SMALL = Font(TYPEFACE_PATH, SMALL_SIZE)
