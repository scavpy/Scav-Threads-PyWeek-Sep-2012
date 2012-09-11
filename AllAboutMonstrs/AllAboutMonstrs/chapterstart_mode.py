import pygame

import chromographs
import gui
import typefaces
import chapters
from modes import ModeOfOperation
from style import PAGECOLOUR, PAGEMARGIN


class ChapterStartMode(ModeOfOperation):
    """ The mode by which one is informed of the current situation. """
    def operate(self, current_situation):
        self.situation = current_situation
        self.initialize()
        self.redraw()
        self.finished = False
        self.next_mode = None
        while not self.finished:
            ms = self.clock.tick(60)
            self.respond_to_the_will_of_the_operator()
        return self.next_mode

    def on_keydown(self, e):
        self.menu.key_event(e)
        if e.key == pygame.K_RETURN:
            choice = self.menu.make_choice()
            if choice:
                if choice == "begin":
                    self.next_mode = "Preparation"
                elif choice == "back":
                    self.next_mode = "Introductory"
                self.finished = True
        self.redraw()

    def on_quit(self, e):
        self.finished = True

    def initialize(self):
        chapter = chapters.CHAPTERS[self.situation.chapter]
        self.ribbon = chromographs.obtain("flourish/ribbon-blue.png")
        self.portrait = chromographs.obtain("illustrations/%s"%chapter.illustration)
        self.title = typefaces.prepare_title("Chapter %s:"% chapter.number)
        self.summary = gui.make_titledbox((400,100),
                                          chapter.subtitle,
                                          chapter.summary,
                                          500,gap=12)
        self.menu = gui.make_menu((700,600),
                                  [("We are prepared!","begin"),
                                   ("We are scared!","back")],300)

    def redraw(self):
        blit = self.screen.blit
        self.clear_screen(colour=PAGECOLOUR)
        blit(self.title,(PAGEMARGIN,PAGEMARGIN))
        blit(self.portrait, (PAGEMARGIN,100))
        self.menu.render(self.screen)
        self.summary.render(self.screen)
        blit(self.ribbon,(850,-2))
        pygame.display.flip()
