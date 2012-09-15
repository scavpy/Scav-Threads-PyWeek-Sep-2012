# -*- encoding: utf-8 -*-
"""
The Encyclopaedia and Almanack of The Colony of ???
"""

import pygame
from pygame.display import get_surface, flip

from modes import ModeOfOperation
import typefaces
import chromographs
import bestiary, units, facilities
import gui

from style import PAGEMARGIN, PAGECOLOUR

PAGES = [
    ("facilities","Housing"),
    ("facilities","Crops"),
    ("facilities","Fence"),
    ("bestiary","Ferociraptor"),
    ("bestiary","Trinitroceratops"),
    ("units","Cannon"),
    ("facilities","Wall"),
    ("bestiary","Tankylosaurus"),
    ("units","AnalyticalCannon"),
    ("bestiary","Blastosaurus"),
    ("bestiary","Explodocus"),
    ]

class EncyclopaediaMode(ModeOfOperation):
    """ Whereby the operator of the device can be presented with
    the fruits of the latest researches in Natural Philosophy """
    def operate(self, current_situation):
        self.situation = current_situation
        self.initialize()
        self.finished = False
        self.next_mode = "ChapterStart" if self.situation.in_game else "Introductory"
        self.backbutton = gui.make_menu((650,600),[("Regress","back")],200)
        self.draw_current_page()
        while not self.finished:
            ms = self.clock.tick(60)
            self.respond_to_the_will_of_the_operator()
            self.draw_current_page()
        return self.next_mode

    def on_quit(self, e):
        self.next_mode = None
        self.finished = True

    def on_keydown(self, e):
        if e.key == pygame.K_ESCAPE:
            self.finished = True
        elif self.page == "index":
            self.index_menu.key_event(e)
            if e.key == pygame.K_RETURN:
                choice = self.index_menu.make_choice()
                self.chosen_from_menu(choice)
        elif e.key == pygame.K_RIGHT:
            page = (self.page + 1) % len(PAGES)
            self.prepare_encyclopaedia_page(page)
        elif e.key == pygame.K_LEFT:
            page = (self.page - 1) % len(PAGES)
            self.prepare_encyclopaedia_page(page)
        elif e.key in (pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_UP):
            self.page = "index"
            self.prepare_index_page()

    def on_mousebuttondown(self, e):
        if self.page == "index":
            choice = self.index_menu.mouse_event(e)
            if choice is not None:
                self.chosen_from_menu(choice)
        else:
            choice = self.backbutton.mouse_event(e)
            if choice:
                self.prepare_index_page()

    def on_mousemotion(self, e):
        self.index_menu.mouse_event(e)

    def chosen_from_menu(self, choice):
        if choice == "regress":
            self.finished = True
        else:
            self.prepare_encyclopaedia_page(choice)

    def initialize(self):
        self.heading = typefaces.prepare_subtitle("Notable Attributes")
        self.index_menu = None
        self.prepare_index_page()
        
    def draw_current_page(self):
        self.clear_screen(colour=PAGECOLOUR)
        if self.page == "index":
            self.show_index_page()
        else:
            self.show_encyclopaedia_page()

    def prepare_encyclopaedia_page(self, page):
        self.page = page
        module, name = PAGES[page]
        if module == "bestiary":
            self.ribbon = chromographs.obtain("flourish/ribbon-red.png")
            article = getattr(bestiary, name)
        elif module =="units":
            self.ribbon = chromographs.obtain("flourish/ribbon-blue.png")
            article = getattr(units, name)
        elif module == "facilities":
            self.ribbon = chromographs.obtain("flourish/ribbon-blue.png")
            article = getattr(facilities, name)
            
        self.title = typefaces.prepare_title(article.name.title())
        notables = [("{0}: ".format(n), getattr(article, n.lower()))
                    for n in article.notable_attributes]
        self.table = typefaces.prepare_table(notables)
        self.information = typefaces.prepare_paragraph(article.__doc__, 600)
        self.illustration = chromographs.obtain(article.depiction)

    def show_encyclopaedia_page(self):
        paint = self.screen.blit
        paint(self.title,(PAGEMARGIN, PAGEMARGIN))
        topy = y = self.title.get_rect().height + 2 * PAGEMARGIN
        x = self.screen.get_size()[0] // 2
        paint(self.heading, (x,y))
        y += self.heading.get_rect().height + PAGEMARGIN
        paint(self.table, (x,y))        
        paint(self.illustration, (PAGEMARGIN, topy))
        paint(self.ribbon,(850,-2))
        self.backbutton.render(self.screen)
        paint(self.information, (PAGEMARGIN, topy + 400 + 2 * PAGEMARGIN))
        flip()

    def prepare_index_page(self):
        self.page = "index"
        self.title = typefaces.prepare_title(u"ENCYCLOPÆDIA")
        if not self.index_menu:
            index_data = [(p[1], i) for (i,p) in enumerate(PAGES)]
            index_data.append(("* Regress *","regress"))
            top = self.title.get_height() + 2*PAGEMARGIN
            self.index_menu = gui.make_menu((300,top), index_data, 400,
                                            prompt="Table of Contents")



    def show_index_page(self):
        paint = self.screen.blit
        paint(self.title,(PAGEMARGIN, PAGEMARGIN))
        self.index_menu.render(self.screen)
        flip()
