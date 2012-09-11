import pygame
from pygame.locals import *

import data
import typefaces
import chromographs
import units
import grid
from modes import ModeOfOperation
from facilities import HorizontalFence, VerticalFence


LOT_COLOUR = (255,255,0,128)
EDGE_COLOUR = (100,255,100,128)
EDGE_HANDLE_RADIUS = 5

class PreparationMode(ModeOfOperation):
    """ The mode in which one invests in construction of defenses
    against impending assault by reptiles.
    """
    def operate(self, current_situation):
        self.initialize()
        self.situation = current_situation

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
        if e.button == 1:
            edge = self.current_edge
            lot = self.current_lot
            if edge:
                aspect = edge.width/edge.height
                fac = VerticalFence(edge) if (aspect<1) else HorizontalFence(edge)
            elif lot:
                fac = units.Cannon(lot)
            else:
                fac = None
            if fac:
                self.situation.add_installation_if_possible(fac)

    def initialize(self):
        self.titletext = typefaces.prepare_title("Prepare for the Onslaught",colour=(255,255,255))
        self.scenery = chromographs.obtain("background.png")
        self.indicate_lot = True
        self.current_edge = None
        self.current_lot = None
        self.townplanner = grid.TownPlanningOffice()
        self.finished = False
        self.result = "Onslaught"

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
        pygame.display.flip()
