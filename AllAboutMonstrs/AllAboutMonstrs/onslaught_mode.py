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

        while not self.finished:
            ms = self.clock.tick(60)
            self.respond_to_the_will_of_the_operator()
            self.render()
        return self.result

    def on_keydown(self, e):
        self.finished = True

    def on_quit(self, e):
        self.result = None
        self.finished = True

    def initialize(self):
        self.titletext = typefaces.prepare_title("Onslaught of Enormities",colour=(255,64,64))
        self.scenery = chromographs.obtain("background.png")
        self.finished = False
        self.result = "Preparation"

    def render(self):
        self.clear_screen(image=self.scenery)
        self.screen.blit(self.titletext,(10,10))

        pygame.display.flip()
