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

        while True:
            ms = self.clock.tick(60)
            
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    return None
                elif event.type == KEYDOWN:
                    return "Onslaught"
            
            self.render()
       
    def initialize(self):
        self.font = pygame.font.Font(data.filepath("Anaktoria.otf"),28)
        self.titletext = self.font.render("Mode of Preparation:",
                                          True, (255,255,255))

    def render(self):
        self.clear_screen(colour=(0,0,100))
        self.screen.blit(self.titletext,(10,10))

        pygame.display.flip()
