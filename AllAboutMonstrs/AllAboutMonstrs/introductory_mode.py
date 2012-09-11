import pygame

import chromographs
from modes import ModeOfOperation
import gui

from style import PAGECOLOUR, PAGEMARGIN

class IntroductoryMode(ModeOfOperation):
    """ The mode serving as an introduction. """
    def operate(self, current_situation):
        self.initialize()
        self.redraw()
        self.finished = False
        self.next_mode = None
        while not self.finished:
            ms = self.clock.tick(60)
            self.respond_to_the_will_of_the_operator()
        return self.next_mode

    def initialize(self):
        self.header = gui.make_textbox((250,PAGEMARGIN),
                                       "BLASTOSAURUS REX",500,
                                       size="title")
        self.menu = gui.make_menu((300,400),
                             [("Initiation","new"),
                              ("Continuation","load"),
                              ("Bestial Education","bestiary"),
                              ("Termination","quit")],400)
        self.ribbon = chromographs.obtain("flourish/ribbon-gold.png")

    def redraw(self):
        self.clear_screen(colour=PAGECOLOUR)
        self.header.render(self.screen)
        self.menu.render(self.screen)
        self.screen.blit(self.ribbon,(850,-2))
        pygame.display.flip()

    def on_keydown(self, e):
        self.menu.key_event(e)
        if e.key == pygame.K_RETURN:
            choice = self.menu.make_choice()
            if choice:
                if choice == "new":
                    self.next_mode = "ChapterStart"
                elif choice == "bestiary":
                    self.next_mode = "Encyclopaedia"
                self.finished = True
        self.redraw()

    def on_quit(self, e):
        self.finished = True
