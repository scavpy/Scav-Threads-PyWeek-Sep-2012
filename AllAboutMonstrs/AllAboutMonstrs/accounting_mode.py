# -*- encoding:utf-8 -*-
"""
 An accounting must be made of the expenses and revenue of the colony
"""
from collections import Counter
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
        # go to the next chapter
        self.situation.chapter += 1
        self.situation.wave = 0
        self.situation.save_game()
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

        def note(label, amount):
            notables.append([label+": ", amount])

        # CACLULATE FOOD
        food = 0
        for item in situation.installations:
            if isinstance(item, facilities.Crops):
                food += max(item.durability - item.damage, 0)

        housing_space = sum([f.habitability
                             for f in self.situation.get_facilities()])

        note("Remaining balance", lsb(situation.wealth))
        note("Housing space", housing_space)
        note("Population", "TBD")
        note("Food produced", food)
        note("Population Growth", "TBD")
        note("Wildlife Samples","TBD")
        note("Income","TBD")
        note("RESULTS","")
        note("  Closing Balance","TBD")
        note("  Current Population","TBD")
        note("  Progress","TBD")

        income = 0
        # Trophies
        cnt = Counter()
        for t in situation.trophies:
            cnt[t] += 1
        for k, v in cnt.items():
            #note(k + " slain", v)
            income += 0x26 * v # 2 shillings and sixbence bounty per corpse
        situation.trophies = []
        
        # Wealth gained
        income += 0x100 * food # 1 pound per sack of cabbages
        situation.wealth += income
        #note("Income", lsb(income))
        #note("Closing balance:", lsb(situation.wealth))

        situation.progress += 100
        #note("Progress", situation.progress)

        # display the report
        paint = self.screen.blit
        self.clear_screen(colour=PAGECOLOUR)
        title = typefaces.prepare_title("Accounting Department")
        paint(title,(PAGEMARGIN, PAGEMARGIN))
        topy = y = title.get_rect().height + 3 * PAGEMARGIN
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
        
