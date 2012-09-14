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
import phonographs
import gui
import chapters
import facilities

from style import PAGEMARGIN, PAGECOLOUR

MEAL_SIZE = 12

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
        phonographs.orchestrate("intromusic.ogg")

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
        # Remaining balance
        remaining_balance = lsb(situation.wealth)

        # Housing space
        housing_space = sum([f.habitability
                             for f in self.situation.get_facilities()])

        # Population
        units = self.situation.get_units()
        for u in units:
            if u.human:
                self.situation.population += 1
                self.situation.installations.remove(u)
        population = self.situation.population
        
        # Food produced
        food_produced = 0
        for item in situation.installations:
            if isinstance(item, facilities.Crops):
                food_produced += max(item.durability - item.damage, 0)

        # Population growth
        food = food_produced
        max_growth_from_crops = food//MEAL_SIZE
        max_growth_from_space = max((housing_space - population),0)
        population_growth = min(max_growth_from_space,
                                max_growth_from_crops)
        if population < 5 and population_growth == 0:
            population_growth = 1
        food -= population_growth*MEAL_SIZE
        # Income from crops
        food_income = food*0x80
        

        note("Remaining balance", remaining_balance)
        note("Housing space", housing_space)
        note("Population", self.situation.population)
        note("Food produced", food_produced)
        note("Population Growth", population_growth)

        trophy_income = 0
        # Trophies
        cnt = Counter()
        for t in situation.trophies:
            cnt[t] += 1
        for k, v in cnt.items():
            note(k + " slain", v)
            trophy_income += 0x26 * v # 2 shillings and sixbence bounty per corpse
        situation.trophies = []
        income = trophy_income + food_income

        note("Income",lsb(income))
        
        # Apply results
        situation.wealth += income
        situation.population += population_growth
        situation.progress += 100
        note("RESULTS","")
        note("  Closing Balance",lsb(situation.wealth))
        note("  Current Population",situation.population)
        note("  Progress",100)

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
        
