import pygame

import bestiary
import chromographs
import phonographs
from modes import ModeOfOperation
import gui

from style import PAGECOLOUR, PAGEMARGIN
import os

class IntroductoryMode(ModeOfOperation):
    """ The mode serving as an introduction. """
    def operate(self, current_situation):
        self.situation = current_situation
        self.situation.in_game = False
        self.initialize()
        self.redraw()
        self.finished = False
        self.next_mode = None
        while not self.finished:
            ms = self.clock.tick(60)
            self.respond_to_the_will_of_the_operator()
            self.redraw()
        return self.next_mode

    def initialize(self):
        if self.situation.args.sheep:
            bestiary.wooly_retribution()
            self.situation.args.sheep = False
        self.header = gui.make_textbox((250,PAGEMARGIN),
                                       "BLASTOSAURUS REX",500,
                                       size="title")
        self.main_menu = gui.make_menu((300,400),
                             [("Initiation","new"),
                              ("Continuation","load"),
                              ("Information","information"),
                              ("Education","encyclopaedia"),
                              ("Termination","quit")],400)
        self.load_menu = self.prepare_load_menu()
        self.name_menu = gui.PunchCard((300,400))
        self.name_prompt = gui.make_textbox(
            (300,200),
            "Punch a card with your name, for the analytical engine:\n",
            400,
            )
        self.menu = self.main_menu
        self.ribbon = chromographs.obtain("flourish/ribbon-white.png")
        phonographs.orchestrate("intromusic.ogg")

    def prepare_load_menu(self):
        savedir = self.situation.get_save_dir()
        saves = [os.path.join(savedir,save)
                 for save in os.listdir(savedir)]
        saves.sort(key=os.path.getmtime, reverse=True)
        saves = [os.path.basename(s) for s in saves][:8]
        savenames = ["%s: Chapter %d"%(s.split("-")[0],int(s.split("-")[1])+1) for s in saves]
        self.load_menu = gui.make_menu((300,150),
                      zip(savenames,saves)+[("Regress","back")],400,
                      prompt="Select Situation")
        return self.load_menu

    def redraw(self):
        self.clear_screen(colour=PAGECOLOUR)
        self.header.render(self.screen)
        self.menu.render(self.screen)
        if self.menu == self.name_menu:
            self.name_prompt.render(self.screen)
        self.screen.blit(self.ribbon,(850,-2))
        pygame.display.flip()

    def on_keydown(self, e):
        self.menu.key_event(e)
        if e.key == pygame.K_RETURN:
            choice = self.menu.make_choice()
            self.chosen_from_menu(choice)

    def on_mousebuttondown(self, e):
        choice = self.menu.mouse_event(e)
        if choice:
            self.chosen_from_menu(choice)

    def on_mousemotion(self, e):
        self.menu.mouse_event(e)

    def chosen_from_menu(self, choice):
        if choice in ["information","encyclopaedia","quit"]:
            if choice == "information":
                self.next_mode = "Information"
            elif choice == "encyclopaedia":
                self.next_mode = "Encyclopaedia"
            self.finished = True
        elif choice == "new":
            self.menu = self.name_menu
        elif choice == "load":
            self.open_load_menu()
        elif choice == "back":
            self.close_load_menu()
        else:
            if self.menu == self.load_menu:
                try:
                    self.situation.load_game(choice)
                    self.next_mode = "ChapterStart"
                    self.finished = True
                except IOError:
                    print("No such save file: %s"%choice)
            elif self.menu == self.name_menu:
                if choice:
                    self.start_new_game(choice)
                else:
                    self.menu = self.main_menu

    def start_new_game(self,name):
        self.situation.reset(name)
        self.situation.land_ho()
        self.situation.save_game()
        self.next_mode = "Exposition"
        self.finished = True

    def open_load_menu(self):
        self.menu = self.load_menu

    def close_load_menu(self):
        self.menu = self.main_menu

    def on_quit(self, e):
        self.finished = True
