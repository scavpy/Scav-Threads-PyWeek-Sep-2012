import pygame
from pygame.locals import *

import data
from modes import ModeOfOperation

class PreparationMode(ModeOfOperation):
    """ The mode in which one invests in construction of defenses
    against impending assault by reptiles.
    """
    def operate(self, current_situation):
        self.initialize()
        result = None

        while not result:
            events = pygame.event.get()
            for event in events:
                if event.type == KEYDOWN:
                    result = "Onslaught"
            
            self.render()

        return result
       
    def initialize(self):
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(data.filepath("Anaktoria.otf"),28)
        self.titletext = self.font.render("Mode of Preparation:",
                                          True, (255,255,255))

    def render(self):
        s = self.screen
        s.fill((0,0,0))
        s.blit(self.titletext,(10,10))

        pygame.display.flip()
