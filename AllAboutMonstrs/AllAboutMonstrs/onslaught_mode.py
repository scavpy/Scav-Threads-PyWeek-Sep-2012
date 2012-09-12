import pygame
from pygame.locals import *
import random

import data
from modes import ModeOfOperation
import chromographs
import typefaces
import units
import bestiary
import chapters

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
        chapter = chapters.CHAPTERS[self.situation.chapter]
        wave = self.situation.wave
        self.dinosaurs = chapter.spawn_wave(wave)
        self.finished = False
        self.result = "Preparation"

    def render(self):
        self.clear_screen(image=self.scenery)
        self.screen.blit(self.titletext,(10,10))

        def render_a_thing(that):
            image = that.image
            position = image.get_rect()
            position.midbottom = that.rect.midbottom
            self.screen.blit(image, position)
        # render flat land first
        for land in (land for land in self.situation.installations
                     if land.is_flat):
            render_a_thing(land)
        # render things that lie upon the land
        to_be_drawn = self.situation.installations + self.dinosaurs
        to_be_drawn.sort(key = lambda d: d.rect.bottom)
        debug_rectangles = self.situation.args.debug_rectangles
        for that in to_be_drawn:
            if that.is_flat:
                continue #already done
            if debug_rectangles:
                pygame.draw.rect(self.screen, (0,255,255), that.rect,1)
                try:
                    pygame.draw.rect(self.screen, (0,255,0), that.rect_of_awareness, 1)
                except AttributeError:
                    pass
                try:
                    pygame.draw.rect(self.screen, (255,200,200), that.rect_of_attack, 1)
                except AttributeError:
                    pass
            render_a_thing(that)
        pygame.display.flip()

    def move_dinosaurs(self, ms):
        all_the_things = self.situation.installations + self.dinosaurs
        for d in self.dinosaurs[:]:
            act = d.animate(ms)
            if act:
                targets = d.think(all_the_things)
            if d.finished:
                self.dinosaurs.remove(d)
                all_the_things.remove(d)
        if not self.dinosaurs:
            self.finished = True

    def move_units(self, ms):
        all_the_things = self.situation.installations + self.dinosaurs
        for u in self.situation.installations:
            act = u.animate(ms)
            if not isinstance(u, units.Unit):
                continue
            if act and u.damage < u.durability:
                targets = u.think(all_the_things)
                if targets:
                    for d in targets:
                        if d.damage >= d.durability:
                            all_the_things.remove(d)
                            self.dinosaurs.remove(d)

                
