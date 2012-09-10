import pygame
from pygame.locals import *

import data
from modes import ModeOfOperation
import chromographs
import typefaces

class OnslaughtMode(ModeOfOperation):
    """ Wherein reptilian foes descend upon you and you must fight them
    lest the colony be destroyed.
    """
    def operate(self, current_situation):
        self.initialize()

        while True:
            ms = self.clock.tick(60)

            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    return None
                elif event.type == KEYDOWN:
                    return "Preparation"

            self.render()

    def initialize(self):
        self.titletext = typefaces.prepare_title("Onslaught of Enormities",colour=(255,64,64))
        self.scenery = chromographs.obtain("background.png")

    def render(self):
        self.clear_screen(image=self.scenery)
        self.screen.blit(self.titletext,(10,10))

        pygame.display.flip()
