"""
The Encyclopaedia and Almanack of The Colony of ???
"""

import pygame
from pygame.display import get_surface, flip

from modes import ModeOfOperation
import typefaces
from bestiary import Animal

PAGES = [
    Animal,
    ]

MARGIN = 24

class EncyclopaediaMode(ModeOfOperation):
    """ Whereby the operator of the device can be presented with
    the fruits of the latest researches in Natural Philosophy """
    def operate(self, current_situation):
        self.page = 0
        self.draw_current_page()
        flip()
        while True:
            for evt in pygame.event.get():
                if evt.type == pygame.KEYDOWN:
                    return

    def draw_current_page(self):
        paint = self.screen.blit
        self.clear_screen(colour=(255,255,240))
        page = PAGES[self.page]
        title = typefaces.prepare_title(page.name.title())
        paint(title,(MARGIN, MARGIN))
        y = title.get_rect().height + MARGIN
        x = self.screen.get_size()[0] // 2
        heading = typefaces.prepare_subtitle("Notable Attributes")
        paint(heading, (x,y))
        y += heading.get_rect().height + MARGIN
        notables = [typefaces.prepare("{0}: {1}".format(n, getattr(page, n.lower())))
                    for n in page.notable_attributes]
        for notable in notables:
            paint(notable, (x, y))
            y += notable.get_rect().height
        information = page.__doc__

        
        
