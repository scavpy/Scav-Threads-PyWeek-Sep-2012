import pygame
from collections import defaultdict

import chromographs
import gui
import typefaces
import chapters
import all_things_known
from modes import ModeOfOperation
from style import PAGECOLOUR, PAGEMARGIN


class ChapterStartMode(ModeOfOperation):
    """ The mode by which one is informed of the current situation. """
    def operate(self, current_situation):
        self.situation = current_situation
        self.situation.in_game = True
        self.initialize()
        self.redraw()
        self.finished = False
        self.next_mode = None
        while not self.finished:
            ms = self.clock.tick(60)
            self.respond_to_the_will_of_the_operator()
            self.redraw()
        return self.next_mode

    def on_keydown(self, e):
        self.menu.key_event(e)
        if e.key == pygame.K_RETURN:
            choice = self.menu.make_choice()
            self.chosen_from_menu(choice)
        self.redraw()

    def on_mousebuttondown(self, e):
        choice = self.menu.mouse_event(e)
        if choice:
            self.chosen_from_menu(choice)

    def on_mousemotion(self, e):
        self.menu.mouse_event(e)

    def chosen_from_menu(self, choice):
        if choice:
            if choice == "begin":
                self.next_mode = "Preparation"
            elif choice == "back":
                self.next_mode = "Introductory"
            elif choice == "encyclopaedia":
                self.next_mode = "Encyclopaedia"
            self.finished = True

    def on_quit(self, e):
        self.finished = True

    def initialize(self):
        situation = self.situation
        chapter = chapters.open_chapter(situation.chapter)
        self.ribbon = chromographs.obtain("flourish/ribbon-white.png")
        self.portrait = chromographs.obtain("illustrations/%s"%chapter.illustration)
        self.title = typefaces.prepare_title("Chapter %s:"% chapter.number)
        self.summary = gui.make_titledbox((400,100),
                                          chapter.subtitle,
                                          chapter.summary,
                                          500,gap=12)
        self.menu = gui.make_menu((700,550),
                                  [("We are prepared!","begin"),
                                   ("We are scared!","back"),
                                   ("Consult Encyclopaedia", "encyclopaedia"),
                                   ],300)
        new_inventions = []
        situation.death_stats = defaultdict(int)
        for name in chapter.inventions:
            if name not in situation.unit_plans:
                new_inventions.append(name)
        for name in chapter.fences:
            if name not in situation.fence_plans:
                new_inventions.append(name)
        for name in chapter.facilities:
            if name not in situation.facility_plans:
                new_inventions.append(name)
        invention_names = [all_things_known.find_by_name(n)
                           for n in new_inventions]
        dinos_in_chapter = chapter.beasts_in_this_chapter()
        dino_names = []
        for name in dinos_in_chapter:
            if name in self.situation.seen_dinosaurs:
                continue
            information = all_things_known.find_by_name(name)
            if information:
                dino_names.append(information.name)
        tabulation = []
        if new_inventions:
            tabulation.append(["NEW INVENTIONS:"])
            tabulation.extend(["    " + n] for n in new_inventions)
        if dino_names:
            tabulation.append(["WATCH OUT FOR:"])
            tabulation.extend(["    " + n] for n in dino_names)
        self.table = None
        if tabulation:
            self.table = typefaces.prepare_table(tabulation)

    def redraw(self):
        blit = self.screen.blit
        self.clear_screen(colour=PAGECOLOUR)
        blit(self.title,(PAGEMARGIN,PAGEMARGIN))
        blit(self.portrait, (PAGEMARGIN,100))
        self.menu.render(self.screen)
        self.summary.render(self.screen)
        blit(self.table, (PAGEMARGIN, 100 + self.portrait.get_height() + PAGEMARGIN))
        blit(self.ribbon,(850,-2))
        pygame.display.flip()
