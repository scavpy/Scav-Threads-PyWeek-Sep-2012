"""
The Encyclopaedia and Almanack of The Colony of ???
"""

import pygame
from pygame.display import get_surface, flip

from modes import ModeOfOperation
import typefaces
import chromographs
from bestiary import Animal

from style import PAGEMARGIN, PAGECOLOUR

PAGES = [
    Animal,
    ]

class EncyclopaediaMode(ModeOfOperation):
    """ Whereby the operator of the device can be presented with
    the fruits of the latest researches in Natural Philosophy """
    def operate(self, current_situation):
        self.page = 0
        self.finished = False
        self.draw_current_page()
        flip()
        while not self.finished:
            ms = self.clock.tick(60)
            self.respond_to_the_will_of_the_operator()
        return

    def on_quit(self, e):
        self.finished = True

    def draw_current_page(self):
        paint = self.screen.blit
        self.clear_screen(colour=PAGECOLOUR)
        page = PAGES[self.page]
        title = typefaces.prepare_title(page.name.title())
        paint(title,(PAGEMARGIN, PAGEMARGIN))
        topy = y = title.get_rect().height + PAGEMARGIN
        x = self.screen.get_size()[0] // 2
        heading = typefaces.prepare_subtitle("Notable Attributes")
        paint(heading, (x,y))
        y += heading.get_rect().height + PAGEMARGIN
        notables = [("{0}: ".format(n), getattr(page, n.lower()))
                    for n in page.notable_attributes]
        table = typefaces.prepare_table(notables)
        paint(table, (x,y))        
        chromograph = chromographs.obtain(page.depiction)
        paint(chromograph, (PAGEMARGIN, topy))
        information = page.__doc__



