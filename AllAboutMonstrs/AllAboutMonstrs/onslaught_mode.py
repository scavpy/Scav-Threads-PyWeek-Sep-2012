import pygame
from pygame.locals import *

import data
from modes import ModeOfOperation

class OnslaughtMode(ModeOfOperation):
    """ Wherein reptilian foes descend upon you and you must fight them
    lest the colony be destroyed.
    """
    def operate(self, current_situation):
        self.initialize()
        result = None

        while not result:
            events = pygame.event.get()
            for event in events:
                if event.type == KEYDOWN:
                    result = "Preparation"
            
            self.render()

        return result
       
    def initialize(self):
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(data.filepath("Anaktoria.otf"),28)
        self.titletext = self.font.render("Mode of Onslaught:",
                                          True, (255,255,255))

    def render(self):
        s = self.screen
        s.fill((0,0,0))
        s.blit(self.titletext,(10,10))

        pygame.display.flip()
