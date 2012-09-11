# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

import data
import typefaces
import chromographs
import facilities
import units
import grid

from gui import BuildMenu
from modes import ModeOfOperation


LOT_COLOUR = (255,255,0,128)
EDGE_COLOUR = (100,255,100,128)
EDGE_HANDLE_RADIUS = 5

class PreparationMode(ModeOfOperation):
    """ The mode in which one invests in construction of defenses
    against impending assault by reptiles.
    """
    def operate(self, current_situation):
        self.situation = current_situation
        self.initialize()

        while not self.finished:
            ms = self.clock.tick(30)
            self.respond_to_the_will_of_the_operator()

            if self.indicate_lot:
                x,y = pygame.mouse.get_pos()
                edge = self.townplanner.nearest_edge(x,y)
                if edge:
                    self.current_edge = edge
                    self.current_lot = None
                else:
                    lot = self.townplanner.nearest_lot(x,y)
                    if lot:
                        self.current_lot = lot
                        self.current_edge = None

            self.render()
        return self.result

    def on_keydown(self, e):
        self.finished = True

    def on_quit(self, e):
        self.result = None
        self.finished = True

    def on_mousebuttondown(self, e):
        if self.build_menu.is_open:
            choice = self.build_menu.mouse_event(e)
            if choice:
                if choice != "CANCEL":
                    self.build_a_thing(choice)
                self.close_build_menu()
        else:
            edge = self.current_edge
            lot = self.current_lot
            if e.button == 1:
                recent = self.situation.most_recent_build
                if recent:
                    self.build_a_thing(recent)
                else:
                    self.open_build_menu(e.pos)
            elif e.button == 3:
                self.open_build_menu(e.pos)

    def open_build_menu(self,position):
        self.build_menu.open_menu(position,self.situation,bool(self.current_edge))
        self.indicate_lot = False

    def close_build_menu(self):
        self.build_menu.close_menu()
        self.indicate_lot = True

    def build_a_thing(self,thingname):
        place = thing = None
        if thingname == "Fence":
            place = self.current_edge
            if place:
                aspect = place.width/place.height
                thing = facilities.VerticalFence if (aspect<1) else facilities.HorizontalFence
        else:
            place = self.current_lot
            if place:
                thing = getattr(facilities,thingname,None)
                if thing is None:
                    thing = getattr(units,thingname,None)
        if thing:
            self.situation.add_installation_if_possible(thing(place))
            self.situation.most_recent_build = thingname
            self.update_stats()

    def initialize(self):
        self.titletext = typefaces.prepare_title("Prepare for the Onslaught",colour=(255,255,255))
        self.scenery = chromographs.obtain("background.png")
        self.indicate_lot = True
        self.current_edge = None
        self.current_lot = None
        self.townplanner = grid.TownPlanningOffice()
        self.finished = False
        self.result = "Onslaught"
        self.build_menu = BuildMenu()
        self.statstable = None
        self.update_stats()

    def update_stats(self):
        s = self.situation
        pounds = s.wealth//256
        shillings = (s.wealth%256)//16
        pence = s.wealth%16
        crops = sum([c.edibility for c in s.installations if hasattr(c,"edibility")])
        table = typefaces.prepare_table([["Wealth: ","£%d/%d/%db"%(pounds,shillings,pence)],
                                         ["Agriculture: ",crops]])
        self.statstable = table
    
    def render(self):
        self.clear_screen(image=self.scenery)
        self.screen.blit(self.titletext,(10,10))
        if self.indicate_lot:
            if self.current_edge:
                pygame.draw.rect(self.screen, EDGE_COLOUR, self.current_edge, 1)
            elif self.current_lot:
                lot = self.current_lot
                pygame.draw.rect(self.screen, LOT_COLOUR, lot, 1)
                for p in [lot.midtop,lot.midbottom,lot.midleft,lot.midright]:
                    pygame.draw.circle(self.screen, EDGE_COLOUR, p, EDGE_HANDLE_RADIUS, 1)
        def render_a_thing(that):
            image = that.image
            position = image.get_rect()
            position.midbottom = that.rect.midbottom
            self.screen.blit(image, position)

        # render flat land first
        for that in self.situation.installations:
            if that.is_flat:
                render_a_thing(that)

        # render things that lie upon the land
        for that in self.situation.installations:
            if that.is_flat:
                continue # already done
            render_a_thing(that)

        if self.build_menu.is_open:
            self.build_menu.render(self.screen)
        self.screen.blit(self.statstable,(10,600))
        pygame.display.flip()
