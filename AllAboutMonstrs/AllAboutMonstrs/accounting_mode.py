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

from style import PAGEMARGIN, PAGECOLOUR

def lsb(bence):
    debit = bence < 0
    if debit:
        bence = -bence
    pounds = bence >> 8
    shillings = bence >> 4 & 0xf
    bence = bence & 0xf
    if not shillings: shillings = "-"
    if not bence: bence = "-"
    fmt = "(£{0} / {1} / {2} b)" if debit else "£{0} / {1} / {2} b"
    return unicode(fmt.format(pounds, shillings, bence), "utf-8")

class AccountingMode(ModeOfOperation):
    """ Whereby the current situation is assessed, and
    stock is taken of the colony's wealth and population """
    def operate(self, current_situation):
        self.situation = current_situation
        self.initialize()
        self.assess()
        self.finished = False
        while not self.finished:
            self.clock.tick(30)
            self.respond_to_the_will_of_the_operator()
        return self.next_mode

    def on_quit(self, e):
        self.next_mode = None
        self.finished = True

    def on_keydown(self, e):
        if e.key == pygame.K_RETURN:
            self.finished = True

    def initialize(self):
        if (self.situation.chapter + 1) >= len(chapters.CHAPTERS):
            # you have won
            self.next_mode = "Victory"
        else:
            # you will proceed to next chapter
            self.next_mode = "ChapterStart"
            # TODO - autosave
        self.ribbon = chromographs.obtain("flourish/ribbon-gold.png")

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
        food = 0
        for item in situation.installations:
            if isinstance(item, facilities.Crops):
                food += item.edibility
        notables.append(["Food produced:", food])

        notables.append(["Wealth:", lsb(situation.wealth)])
        
        # display the report
        paint = self.screen.blit
        self.clear_screen(colour=PAGECOLOUR)
        title = typefaces.prepare_title("Accounting Department")
        paint(title,(PAGEMARGIN, PAGEMARGIN))
        topy = y = title.get_rect().height + PAGEMARGIN
        x = self.screen.get_size()[0] // 2
        heading = typefaces.prepare_subtitle("Ledger Entries")
        paint(heading, (x,y))
        y += heading.get_rect().height + PAGEMARGIN
        table = typefaces.prepare_table(notables)
        paint(table, (x,y))        
        chromograph = chromographs.obtain("Accountant.png")
        paint(chromograph, (PAGEMARGIN, topy))
        paint(self.ribbon,(850,-2))
        flip()
        
