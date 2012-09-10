import pygame
from pygame.locals import *

import data
import typefaces
import chromographs
import grid
from modes import ModeOfOperation

class PreparationMode(ModeOfOperation):
    """ The mode in which one invests in construction of defenses
    against impending assault by reptiles.
    """
    def operate(self, current_situation):
        self.initialize()

        while not self.finished:
            ms = self.clock.tick(30)
            self.respond_to_the_will_of_the_operator()

            if self.indicate_lot:
                x,y = pygame.mouse.get_pos()
                lot = self.townplanner.nearest_lot(x,y)
                if lot:
                    self.current_lot = lot

            self.render()
        return self.result

    def on_keydown(self, e):
        self.finished = True

    def on_quit(self, e):
        self.result = None
        self.finished = True

    def initialize(self):
        self.titletext = typefaces.prepare_title("Prepare for the Onslaught",colour=(255,255,255))
        self.scenery = chromographs.obtain("background.png")
        self.indicate_lot = True
        self.current_lot = None
        self.townplanner = grid.TownPlanningOffice()
        self.finished = False
        self.result = "Onslaught"

    def render(self):
        self.clear_screen(image=self.scenery)
        self.screen.blit(self.titletext,(10,10))
        if self.indicate_lot and self.current_lot:
            pygame.draw.rect(self.screen, (255,255,0,128), self.current_lot, 1)
        pygame.display.flip()
