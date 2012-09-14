# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

import data
import typefaces
import phonographs
import chromographs
import facilities
import units
import grid

from gui import BuildMenu, StatusBar
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
                if choice == "REPAIR":
                    self.repair_facility(self.build_menu.repairable)
                else:
                    self.build_a_thing(choice)
            self.close_build_menu()
        else:
            edge = self.current_edge
            lot = self.current_lot
            if e.button == 1:
                thing = self.situation.last_build
                built = False
                if thing:
                    fence = bool(thing.obstruance & grid.obstruance("fence"))
                    if (edge and fence) or (lot and not fence):
                        self.build_a_thing(thing)
                        built = True
                if not built:
                    self.open_build_menu(e.pos)
            elif e.button == 3:
                self.open_build_menu(e.pos)

    def open_build_menu(self,position):
        fac = self.get_hovered_facility(position)
        self.build_menu.open_menu(position,repairable=fac,edge=bool(self.current_edge))
        self.indicate_lot = False

    def close_build_menu(self):
        self.build_menu.close_menu()
        self.indicate_lot = True

    def get_hovered_facility(self,pos):
        choices = []
        facilities = self.situation.get_facilities()
        for f in facilities:
            rect = f.image.get_rect()
            rect.midbottom = f.rect.midbottom
            if rect.collidepoint(pos):
                choices.append(f)
        if choices:
            choices.sort(key=lambda x: x.rect.bottom, reverse=True)
            fac = choices[0]
            return fac
        return None

    def repair_facility(self, facility):
        cost = int((float(facility.damage)/facility.durability)
                   *facility.cost)
        if cost <= self.situation.wealth:
            facility.repair()
            self.situation.wealth -= cost
            self.situation.update_status_bar(self.statusbar)

    def build_a_thing(self,thingclass):
        if self.situation.can_afford_a(thingclass):
            place = self.current_edge if self.current_edge else self.current_lot
            if place:
                self.situation.add_installation_if_possible(thingclass(place),charge=True)
                if hasattr(thingclass,"placement_phonograph"):
                    phonographs.play(thingclass.placement_phonograph)
                self.situation.last_build = thingclass
                self.situation.update_status_bar(self.statusbar)

    def initialize(self):
        self.titletext = typefaces.prepare_title("Prepare for the Onslaught",colour=(255,255,255))
        self.scenery = chromographs.obtain("background.png")
        self.indicate_lot = True
        self.current_edge = None
        self.current_lot = None
        self.townplanner = grid.TownPlanningOffice()
        self.finished = False
        self.result = "Onslaught"
        situation = self.situation
        self.build_menu = BuildMenu(situation)
        self.statusbar = StatusBar()
        situation.update_status_bar(self.statusbar)
        for inst in situation.installations[:]:
            if inst.destroyed():
                situation.installations.remove(inst)
        for unit in situation.get_units():
            unit.damage = 0 # repair units automatically
            unit.attacking = 0
            unit.animation_frame = 1
            unit.image = unit.obtain_frame()
        phonographs.orchestrate("intromusic.ogg")
    
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

        self.statusbar.render(self.screen)
        if self.build_menu.is_open:
            self.build_menu.render(self.screen)
        pygame.display.flip()
