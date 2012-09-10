import pygame
from pygame.locals import *

import data
import typefaces
import chromographs
from modes import ModeOfOperation

class PreparationMode(ModeOfOperation):
    """ The mode in which one invests in construction of defenses
    against impending assault by reptiles.
    """
    def operate(self, current_situation):
        self.initialize()

        while True:
            ms = self.clock.tick(30)

            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    return None
                elif event.type == KEYDOWN:
                    return "Onslaught"

            self.render()

    def initialize(self):
        self.titletext = typefaces.prepare_title("Prepare for the Onslaught",colour=(255,255,255))
        self.scenery = chromographs.obtain("background.png")

    def render(self):
        self.clear_screen(image=self.scenery)
        self.screen.blit(self.titletext,(10,10))
        pygame.display.flip()
