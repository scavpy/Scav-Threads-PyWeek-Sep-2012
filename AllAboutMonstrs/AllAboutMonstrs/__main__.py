import pygame

import modes

def main():
    """ Here begins the operation of the analytical engine """
    pygame.init()
    current_situation = {}
    shepherd = modes.ShepherdOfModes()
    shepherd.begin("DoingNoThing", current_situation)
    pygame.quit()
