# -*- encoding:utf-8 -*-
"""
 An accounting must be made of the expenses and revenue of the colony
"""

import pygame
from pygame.display import get_surface, flip

from modes import ModeOfOperation
import typefaces
import chromographs
import phonographs
import gui
import chapters
import facilities

from accounting_mode import lsb

from style import PAGEMARGIN, PAGECOLOUR

class VictoryMode(ModeOfOperation):
    """ Whereby the finale situation is assessed, and
    victory is celebrated """
    def operate(self, current_situation):
        self.situation = current_situation
        self.initialize()
        self.assess()
        self.finished = False
        while not self.finished:
            ms = self.clock.tick(30)
            self.credits.advance(ms)
            self.respond_to_the_will_of_the_operator()
            self.redraw()
        # go to the intro screen
        return "Introductory"

    def on_quit(self, e):
        self.next_mode = None
        self.finished = True

    def on_keydown(self, e):
        if e.key == pygame.K_RETURN:
            self.finished = True

    def initialize(self):
        self.ribbons = [chromographs.obtain("flourish/ribbon-{0}.png"
                                            .format(c))
                        for c in ("red","white","blue")]
        phonographs.orchestrate("victory.ogg", once=True)
        location = pygame.Rect(PAGEMARGIN,100,500,600)
        self.credits = gui.SelfAdvancingScroll(CREDITS, location, 20)
        self.title = typefaces.prepare_title("Victory is Yours")
        self.heading = typefaces.prepare_subtitle("Final Ledger Entries")
        
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
            
        note("Final balance", lsb(situation.wealth))
        note("Final progress", situation.progress)
        self.table = typefaces.prepare_table(notables)

    def redraw(self):
        # display the report
        paint = self.screen.blit
        self.clear_screen(colour=PAGECOLOUR)
        
        paint(self.title,(PAGEMARGIN, PAGEMARGIN))
        topy = y = self.title.get_rect().height + PAGEMARGIN
        x = PAGEMARGIN*2 + 500
        paint(self.heading, (x,y))
        y += self.heading.get_rect().height + PAGEMARGIN
        paint(self.table, (x,y))        
        for i, r in enumerate(self.ribbons):
            paint(r,(850 + 30 * i,-2))
        self.credits.render(self.screen)
        flip()
        
CREDITS = u"""
⸙ Blastosaurus Rex ⸙

An entertainment in the form of an interactive
experience, performed upon the analytical engine.

Chief Engineer:  Mr P Scavenger (scav)
2nd Engineer: Mr Ichabod Threadworthy (Threads)

The above take full responsibility for the parlous
state of the artistic depictions and shoddy
construction of the algorithmic installations.

Our praise and gratitude goes to the following:

☞ Mr George Douros for his superb Anaktoria font.
(http://www.fonts2u.com/anaktoria.font)

☞ The Skidmore College Orchestra for their
delightful rendition of Tchaikovsky's 1812 Overture.
(http://www.classiccat.net/tchaikovsky_pi/49.php)

☞ The African Grey Parrot, for various sounds

☞ The wife and the girlfriend of the engineers, for
their patience.

☞ Miscellaneous auditory fragments from
(http://FreeSound.org)


Our condemnation, opprobrium and censure fall on:

☞ The audio system on Linux; specificially jackd,
pulseaudio, ALSA and all combinations and
interactions thereof and between, that make it
nearly impossible to install a working audio
system and sound editing software.
"""
