"""
The Encyclopaedia and Almanack of The Colony of ???
"""

import pygame
from pygame.display import get_surface, flip

from modes import ModeOfOperation
import typefaces
import chromographs
import bestiary, units
import gui

from style import PAGEMARGIN, PAGECOLOUR

PAGES = [
    ("bestiary","Trinitroceratops"),
    ("units","Cannon"),
    ]

class EncyclopaediaMode(ModeOfOperation):
    """ Whereby the operator of the device can be presented with
    the fruits of the latest researches in Natural Philosophy """
    def operate(self, current_situation):
        self.page = 0
        self.finished = False
        self.next_mode = None
        self.backbutton = gui.make_menu((650,600),[("Regress","back")],200)
        self.draw_current_page()
        while not self.finished:
            ms = self.clock.tick(60)
            self.respond_to_the_will_of_the_operator()
        return self.next_mode

    def on_keydown(self, e):
        if e.key in (pygame.K_RETURN,pygame.K_ESCAPE):
            self.next_mode = "Introductory"
            self.finished = True
        elif e.key == pygame.K_RIGHT:
            self.page = (self.page + 1) % len(PAGES)
            self.draw_current_page()
        elif e.key == pygame.K_LEFT:
            self.page = (self.page - 1) % len(PAGES)
            self.draw_current_page()

    def on_quit(self, e):
        self.finished = True

    def draw_current_page(self):
        paint = self.screen.blit
        self.clear_screen(colour=PAGECOLOUR)
        module, name = PAGES[self.page]
        if module == "bestiary":
            self.ribbon = chromographs.obtain("flourish/ribbon-red.png")
            page = getattr(bestiary, name)
        elif module =="units":
            self.ribbon = chromographs.obtain("flourish/ribbon-blue.png")
            page = getattr(units, name)
        title = typefaces.prepare_title(page.name.title())
        paint(title,(PAGEMARGIN, PAGEMARGIN))
        topy = y = title.get_rect().height + 2 * PAGEMARGIN
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
        paint(self.ribbon,(850,-2))
        self.backbutton.render(self.screen)
        information = typefaces.prepare_paragraph(page.__doc__, 600)
        paint(information, (PAGEMARGIN, topy + 400 + 2 * PAGEMARGIN))
        flip()


