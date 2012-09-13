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
    ("Information Pages",None,"In these tip screens, as well as in the \
enyclopaedia of species and technology, the left and right arrow keys \
will turn the pages."),
    ("The Objective","fleet.png","The objective of the game is to \
protect your fleet. After all, if you lose them, you can never return \
home. You can do this by building facilities and units before the \
battle. Some units can also be commanded during the battle."),
    ("Preparing for Battle","build-menu.png","When you begin a chapter \
the first phase is the preparation phase. During the phase you can \
right click to open the build menu. Most items cost money, but \
soldiers can be deployed for free if you have troops in reserve.\n \
Clicking on a cell will allow you to build units or facilities. \
Clicking on a cell edge will allow you to build fences and walls."),
    ("The Status Bar","status-bar.png","Wealth is measured in pounds, \
shillings, and binary pence. A shilling is worth 16 bence while a pound \
is worth 16 shillings. Placing crops will increase your food, and if you \
also build housing, you will gain more troops after the chapter is \
complete.\n The little icon to the right of these stats represents \
the last item you have built and the item that you can build by \
left-clicking. To the right of this, icons show you how many of your \
ships remain undestroyed."),
    ]

TIPS = ["An entire field of crops (12 food) will gain you one more \
troop at the end of the chapter, if you have housing for them.",
        ]

class InformationMode(ModeOfOperation):

    def operate(self, current_situation):
        self.page = 0
        self.finished = False
        self.backbutton = gui.make_menu((650,600),[("Regress","back")],200)
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

    def on_quit(self, e):
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
