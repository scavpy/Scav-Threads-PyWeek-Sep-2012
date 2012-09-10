import pygame
from pygame.locals import *
import random

import data
from modes import ModeOfOperation
import chromographs
import typefaces
import units

class OnslaughtMode(ModeOfOperation):
    """ Wherein reptilian foes descend upon you and you must fight them
    lest the colony be destroyed.
    """
    def operate(self, current_situation):
        self.situation = current_situation
        self.initialize()

        while not self.finished:
            ms = self.clock.tick(60)
            self.respond_to_the_will_of_the_operator()
            self.move_dinosaurs(ms)
            self.move_units(ms)
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
        self.dinosaurs = []
        self.finished = False
        self.result = "Preparation"

    def render(self):
        self.clear_screen(image=self.scenery)
        self.screen.blit(self.titletext,(10,10))
        to_be_drawn = self.situation.installations + self.dinosaurs
        to_be_drawn.sort(key = lambda d: d.rect.bottom)
        for that in to_be_drawn:
            image = that.image
            position = image.get_rect()
            position.midbottom = that.rect.midbottom
            self.screen.blit(image, position)            
        pygame.display.flip()

    def move_dinosaurs(self, ms):
        pass

    def move_units(self, ms):
        # make cannon fire randomly
        for u in self.situation.installations:
            u.animate(ms)
            if isinstance(u, units.Cannon):
                if random.random() < 0.01:
                    u.attack()
                
