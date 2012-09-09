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
        title = typefaces.TITLE.render(page.name.title(), True, (0,0,0))
        paint(title,(MARGIN, MARGIN))
        y = title.get_rect().height + MARGIN
        x = self.screen.get_size()[0] // 2
        heading = typefaces.SUBTITLE.render("Notable Attributes",True, (0,0,0))
        paint(heading, (x,y))
        y += heading.get_rect().height + MARGIN
        notables = [typefaces.NORMAL.render("{0}: {1}"
                                            .format(n, getattr(page, n.lower())),
                                            True, (0,0,0))
                    for n in page.notable_attributes]
        for notable in notables:
            paint(notable, (x, y))
            y += notable.get_rect().height
        information = page.__doc__

        
        
