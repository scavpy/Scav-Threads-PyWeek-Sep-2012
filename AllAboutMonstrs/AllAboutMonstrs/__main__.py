import pygame

import sys
import os

here = os.path.abspath(os.path.dirname(__file__))
sys.path.append(here)

import modes
import situation
import phonographs
import bestiary

SCREENRES = (1024,768)

def main(args):
    """ Here begins the operation of the analytical engine """
    pygame.display.init()
    pygame.mixer.init()
    flags = pygame.FULLSCREEN if args.full else 0
    screen = pygame.display.set_mode(SCREENRES, flags)
    pygame.display.set_caption("Blastosaurus Rex")
    current_situation = situation.Situation()
    current_situation.args = args
    shepherd = modes.ShepherdOfModes()
    start_state = args.test_start_state if args.test_start_state else "Introductory"
    shepherd.begin(start_state, current_situation)
    pygame.quit()
            
        
