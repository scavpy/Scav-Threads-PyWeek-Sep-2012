import pygame

import sys
import os

here = os.path.abspath(os.path.dirname(__file__))
sys.path.append(here)

import modes

SCREENRES = (1024,768)

def main():
    """ Here begins the operation of the analytical engine """
    pygame.init()
    screen = pygame.display.set_mode(SCREENRES)
    pygame.display.set_caption("Blastosaurus Rex")
    current_situation = {}
    shepherd = modes.ShepherdOfModes()
    shepherd.begin("DoingNoThing", current_situation)
    pygame.quit()
