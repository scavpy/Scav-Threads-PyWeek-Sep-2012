# -*- encoding:utf-8 -*-
"""
 An accounting must be made of the expenses and revenue of the colony
"""

import pygame
from pygame.display import get_surface, flip

from modes import ModeOfOperation
import typefaces
import chromographs
import gui
import chapters
import facilities

from accounting_mode import lsb

from style import PAGEMARGIN, PAGECOLOUR

class VictoryMode(ModeOfOperation):
    """ Whereby the finale situation is assessed, and
    victory is celebrated """
    def operate(self, current_situation):
        self.situation = current_situation
        self.initialize()
        self.assess()
        self.finished = False
        while not self.finished:
            self.clock.tick(30)
            self.respond_to_the_will_of_the_operator()
        # go to the intro screen
        return "Introductory"

    def on_quit(self, e):
        self.next_mode = None
        self.finished = True

    def on_keydown(self, e):
        if e.key == pygame.K_RETURN:
            self.finished = True

    def initialize(self):
        self.ribbons = [chromographs.obtain("flourish/ribbon-{0}.png"
                                            .format(c))
                        for c in ("red","white","blue")]

    def assess(self):
        """
        Surviving housing raises the cap on maximum population.

        Surviving crops and sheep produce food. This grows the
        population up to the maximum, and thereafter counts to wealth.

        Surviving industrial buildings increase wealth.

        Surviving population increase technological progress and
        themselves count towards population growth.

        Killed but not exploded dinosaurs count to wealth (fuel).
        """
        situation = self.situation
        notables = []
        for item in situation.installations:
            if isinstance(item, facilities.Crops):
                food += item.edibility

        def note(label, amount):
            notables.append([label+": ", amount])
            
        note("Final balance", lsb(situation.wealth))
        note("Final progress", situation.progress)

        # display the report
        paint = self.screen.blit
        self.clear_screen(colour=PAGECOLOUR)
        title = typefaces.prepare_title("Victory is Yours")
        paint(title,(PAGEMARGIN, PAGEMARGIN))
        topy = y = title.get_rect().height + PAGEMARGIN
        x = self.screen.get_size()[0] // 2
        heading = typefaces.prepare_subtitle("Final Ledger Entries")
        paint(heading, (x,y))
        y += heading.get_rect().height + PAGEMARGIN
        table = typefaces.prepare_table(notables)
        paint(table, (x,y))        
        chromograph = chromographs.obtain("Victory.png")
        paint(chromograph, (PAGEMARGIN, topy))
        for i, r in enumerate(self.ribbons):
            paint(r,(820 + 30 * i,-2))
        flip()
        
