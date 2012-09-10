import pygame

import gui

class IntroductoryMode(ModeOfOperation):
    """ The mode serving as an introduction. """
    def operate(self, current_situation):
        self.initialize()

    def initialize(self):
        self.header = gui.make_textbox((250,18),"BLASTOSAURUS REX",
                                  500,size="title")
        self.menu = gui.make_menu((300,400),
                             [("Initiation","new"),
                              ("Continuation","load"),
                              ("Bestiary","bestiary")],400)
