import pygame

import chromographs
import gui
import typefaces
import chapters
from modes import ModeOfOperation
from style import PAGECOLOUR, PAGEMARGIN

PREMISE = """Her Majesty Queen Victoria III Commands:

 That a colony of the British Empire be established
 in the untamed wilderness of New Cumbria, where there
 are said to be untapped mineral resources and zoological
 wonders.

 And that {0} be appointed governor of said colony.

 It is of vital importance to establish this colony
 for the glory of the British Empire and Her Majesty,
 lest its wealth falls into the hands of the Belgian Empire
 or the Welsh Republic.
 
 Since all previous expeditions have not returned, you
 have been supplied with four ironclad ships and
 all the supplies both military and scientific that
 are deemed requisite.

 If you succeed where so many have previously failed
 you will return to great wealth and Royal favour.


 
 If you fail, you needn't trouble to return.

 God Save The Queen
"""

class ExpositionMode(ModeOfOperation):
    """ The mode by which the premise is communicated to
    a new initiate to the entertainment. """
    def operate(self, current_situation):
        self.name = current_situation.savename
        self.initialize()
        self.redraw()
        self.finished = False
        self.next_mode = "ChapterStart"
        while not self.finished:
            ms = self.clock.tick(60)
            self.exposition.advance(ms)
            self.respond_to_the_will_of_the_operator()
            self.redraw()
        return self.next_mode

    def on_quit(self, e):
        self.next_mode = None
        self.finished = True

    def initialize(self):
        self.title = typefaces.prepare_title("Blastosaurus Rex")
        self.subtitle = typefaces.prepare_subtitle(
            "Adventures in the Land of No Return")
        self.ribbon = chromographs.obtain("flourish/ribbon-white.png")
        self.title_top = PAGEMARGIN
        self.subtitle_top = PAGEMARGIN + self.title_top + self.title.get_height()
        scroll_top = PAGEMARGIN + self.subtitle_top + self.subtitle.get_height()
        width = 800
        height = 480
        location = pygame.Rect(PAGEMARGIN, scroll_top, width, height)
        self.exposition = gui.SelfAdvancingScroll(PREMISE.format(self.name), location, 30)

    def redraw(self):
        blit = self.screen.blit
        self.clear_screen(colour=PAGECOLOUR)
        blit(self.title,(PAGEMARGIN, self.title_top))
        blit(self.subtitle, (PAGEMARGIN, self.subtitle_top))
        blit(self.ribbon,(850,-2))
        self.exposition.render(self.screen)
        pygame.display.flip()

    def on_keydown(self, evt):
        if evt.key == pygame.K_DOWN:
            self.exposition.advance_rapidly()
        elif evt.key == pygame.K_UP:
            self.exposition.regress_rapidly()
        elif evt.key == pygame.K_RETURN:
            self.finished = True

    def on_keyup(self, evt):
        if evt.key == pygame.K_DOWN:
            self.exposition.advance_slowly()
        elif evt.key == pygame.K_UP:
            self.exposition.advance_slowly()

    def on_mousebuttondown(self, evt):
        amount = 160
        if evt.button == 1:
            self.finished = True
        elif evt.button == 4:
            self.exposition.regress_rapidly()
            self.exposition.advance(amount)
            self.exposition.advance_slowly()
        elif evt.button == 5:
            self.exposition.advance_rapidly()
            self.exposition.advance(amount)
            self.exposition.advance_slowly()



