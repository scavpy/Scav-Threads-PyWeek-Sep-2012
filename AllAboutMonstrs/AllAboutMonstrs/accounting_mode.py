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
        if self.defeated:
            current_situation.reload_game()
        else:
            self.situation.chapter += 1
            self.situation.wave = 0
            self.situation.save_game()
        return self.next_mode

    def on_quit(self, e):
        self.next_mode = None
        self.finished = True

    def on_keydown(self, e):
        if e.key in [pygame.K_RETURN,pygame.K_SPACE]:
            self.finished = True

    def on_mousebuttondown(self, e):
        if e.button == 1:
            self.finished = True

    def initialize(self):
        self.next_mode = "ChapterStart"
        self.defeated = not self.situation.ships_remaining()

        if not self.defeated and self.situation.chapter >= chapters.last_chapter():
            self.next_mode = "Victory"

        colour = "black" if self.defeated else "gold"
        self.ribbon = chromographs.obtain("flourish/ribbon-{0}.png".format(colour))
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
        progress = 0
        notables = []
        income = 0
        population_growth = 0
        
        def note(label, amount):
            notables.append([label+": ", amount])

        if not self.defeated:
            # Remaining balance
            remaining_balance = gui.lsb(situation.wealth)

            # Housing space
            housing_space = sum([f.habitability
                                 for f in self.situation.get_facilities()])
            progress += housing_space

            # Population
            units = self.situation.get_units()
            for u in units:
                if u.human:
                    self.situation.population += 1
                    self.situation.installations.remove(u)
                    u.promote()
                    progress += 10 * u.rank
                    self.situation.reserves.append(u)
            population = self.situation.population

            # Food produced
            food_produced = self.situation.count_food()

            # Population growth
            food = food_produced
            max_growth_from_crops = food//MEAL_SIZE
            max_growth_from_space = max((housing_space - population),0)
            population_growth = min(max_growth_from_space,
                                    max_growth_from_crops)
            food -= population_growth*MEAL_SIZE
            if population < 5 and population_growth < 3:
                population_growth = 3
            # Income from crops
            income += food*0x80


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
            progress += 5
        for k, v in cnt.items():
            note(k + " slain", v)
            trophy_income += 0x100 * v # 1 pound bounty per dinosaur
        situation.trophies = []
        income += trophy_income + 0x100 # 1 pound bonus

        if not self.defeated:
            note("Income", gui.lsb(income))

        # Death stats
        for (k,v) in self.situation.death_stats.items():
            note("Men " + k, v)
            
        # Apply results
        situation.wealth += income
        situation.population += population_growth
        situation.progress += progress
        note("RESULTS","")
        note("  Closing Balance", gui.lsb(situation.wealth))
        note("  Current Population",situation.population)
        note("  Progress", progress)

        # display the report
        paint = self.screen.blit
        self.clear_screen(colour=PAGECOLOUR)
        caption = "You Were Defeated" if self.defeated else "Accounting Department"
        title = typefaces.prepare_title(caption)
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
        
