"""
All information about planning and warfare.
"""

import pygame
from pygame.display import get_surface, flip

from modes import ModeOfOperation
import typefaces
import chromographs
import gui

from style import PAGEMARGIN, PAGECOLOUR

HELP = [
    ("Information Pages",None,"In these tip screens, as well as in the "
     "enyclopaedia of species and technology, the left and right arrow "
     "keys will turn the pages."),
    ("The Objective","boat.png","The objective of the game is to "
     "protect your fleet. After all, if you lose them, you can never "
     "return home. You can do this by building facilities and units "
     "before the battle. Some units can also be commanded during the "
     "battle."),
    ("Preparing for Battle","build-menu.png","When you begin a chapter "
     "the first phase is the preparation phase. During the phase you "
     "can right click to open the build menu. Most items cost money, "
     "but soldiers can be deployed for free if you have troops in "
     "reserve.\n"
     "Clicking on a cell will allow you to build units or facilities. "
     "Clicking on a cell edge will allow you to build fences and walls."),
    ("The Status Bar","status-bar.png","Wealth is measured in pounds, "
     "shillings, and binary pence. A shilling is worth 16 bence while "
     "a pound is worth 16 shillings. Food will gain you troops after "
     "the battle, if you have housing for them, and is gained by "
     "planting crops.\n "
     "The little icon to the right of these stats represents the last "
     "item you have built and the item that you can build by "
     "left-clicking. On the far right, beyond some help messages, are "
     "icons representing how many undestroyed ships you have remaining."),
    ("Crops and Housing","domestic.png","Placing crops and housing won't "
     "protect you from dinosaurs. However, when you finish the chapter, "
     "each untouched field of crops (or 12 food) will grant you an extra "
     "soldier for next chapter. You can only have as many soldiers as you "
     "have housing for however. Each house has space for three soldiers and "
     "ships provide an extra two each.\n "
     "Any extra food you have will be converted to wealth."),
    ("The Onslaught","combat.png","When you begin the Onslaught, you will "
     "have nothing but your soldiers and artillery to protect you. You can "
     "direct your soldiers around by clicking on them and then to a "
     "destination.\n "
     "Simple cannons will need a soldier to operate them, they "
     "will only fire if there is at least one soldier nearby. Perhaps one "
     "day, modern science will change this, but for now, battle stations men!")
    ]

TIPS = ["An entire field of crops (12 food) will gain you one more \
troop at the end of the chapter, if you have housing for them.",
        ]

class InformationMode(ModeOfOperation):

    def operate(self, current_situation):
        self.page = 0
        self.finished = False
        self.backbutton = gui.make_menu((650,600),[("Regress","back")],200)
        self.next_mode = "Introductory"
        self.draw_current_page()
        while not self.finished:
            ms = self.clock.tick(60)
            self.respond_to_the_will_of_the_operator()
        return self.next_mode

    def on_keydown(self, e):
        if e.key in (pygame.K_RETURN, pygame.K_ESCAPE):
            self.next_mode = "Introductory"
            self.finished = True
        elif e.key == pygame.K_RIGHT:
            self.page = (self.page + 1) % len(HELP)
            self.draw_current_page()
        elif e.key == pygame.K_LEFT:
            self.page = (self.page - 1) % len(HELP)
            self.draw_current_page()

    def on_mousebuttondown(self,e):
        choice = self.backbutton.mouse_event(e)
        if choice:
            self.next_mode = "Introductory"
            self.finished = True

    def on_quit(self, e):
        self.next_mode = None
        self.finished = True

    def draw_current_page(self):
        paint = self.screen.blit
        self.clear_screen(colour=PAGECOLOUR)
        title, image, desc = HELP[self.page]
        if image is None:
            image = "book.png"
        self.ribbon = chromographs.obtain("flourish/ribbon-blue.png")
        titleline = typefaces.prepare_title(title)
        paint(titleline,(PAGEMARGIN,PAGEMARGIN))
        topy = y = titleline.get_rect().height + 2 * PAGEMARGIN
        x = self.screen.get_size()[0] // 2
        chromograph = chromographs.obtain("illustrations/%s"%image)
        paint(chromograph, (PAGEMARGIN, topy))
        paint(self.ribbon,(850,-2))
        passage = gui.make_textbox((500,topy+100),desc,500)
        passage.render(self.screen)
        self.backbutton.render(self.screen)

        flip()
