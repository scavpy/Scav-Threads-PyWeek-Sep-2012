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

MARGIN = 10

class EncyclopaediaMode(ModeOfOperation):
    """ Whereby the operator of the device can be presented with
    the fruits of the latest researches in Natural Philosophy """
    def operate(self, current_situation):
        self.page = 0
        self.disp = get_surface()
        self.draw_current_page()
        flip()
        while True:
            for evt in pygame.event.get_events():
                if evt.type = pygame.KEYDOWN:
                    return

    def draw_current_page(self):
        disp = self.disp
        disp.fill((255,255,240))
        page = PAGES[self.page]
        title = typefaces.TITLE.render(page.name, True, (0,0,0))
        disp.render(title,(MARGIN, MARGIN))
        y = title.get_rect().height + MARGIN
        x = disp.get_size()[0] // 2
        heading = typefaces.SUBTITLE.render("Notable Attributes",True, (0,0,0))
        disp.render(heading, (x,y))
        y += heading.get_rect().height + MARGIN
        labels = [typeface.NORMAL.render(n, True, (0,0,0))
                  for n in page.notable_attributes]
        values = [getattr(page, n.lower())
                  for n in page.notable_attributes]
        for i, (lab, val) in enumerate(zip(labels, values)):
            pass

        
        
