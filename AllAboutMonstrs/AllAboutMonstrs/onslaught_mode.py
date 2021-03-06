import pygame
from pygame.locals import *
import random

import data
from modes import ModeOfOperation
import gui
import chromographs
import phonographs
import typefaces
import units
import bestiary
import chapters
import visual_effects

class OnslaughtMode(ModeOfOperation):
    """ Wherein reptilian foes descend upon you and you must fight them
    lest the colony be destroyed.
    """
    def operate(self, current_situation):
        self.situation = current_situation
        self.initialize()

        while not self.finished:
            ms = self.clock.tick(60)
            self.respond_to_the_will_of_the_operator()
            self.move_dinosaurs(ms)
            self.move_units(ms)
            self.situation.update_status_bar(self.statusbar)
            self.render()
            self.dead_test()
            self.win_test()
        phonographs.play("fanfare.ogg")
        phonographs.diminuendo(1000)
        # calculate the death statistics
        for u in self.situation.installations:
            if u.human and u.destroyed():
                self.situation.death_stats[u.killed_by] += 1
        return self.result

    def on_keydown(self, e):
        if e.key == pygame.K_w:
            print "Dinosaurs:", self.dinosaurs
            self.finished = True

    def on_quit(self, e):
        self.result = None
        self.finished = True

    def on_mousebuttondown(self,e):
        choices = self.get_units_at(e.pos)
        if self.selected_unit:
            if not choices:
                self.selected_unit.destination = e.pos
            else:
                choice = None
                for c in choices:
                    if c != self.selected_unit:
                        choice = c
                        break
                self.selected_unit = choice
        else:
            if choices:
                self.selected_unit = choices[0]
        if self.selected_unit:
            self.situation.last_build = self.selected_unit.__class__
            self.situation.update_status_bar(self.statusbar)
            name = self.selected_unit.name_and_rank() if self.selected_unit.human else None
            self.statusbar.set_unit_name(name)

    def get_units_at(self,pos):
        choices = []
        units = self.situation.get_units()
        for u in units:
            rect = u.image.get_rect()
            rect.midbottom = u.rect.midbottom
            if rect.collidepoint(pos):
                choices.append(u)
        if choices:
            choices.sort(key=lambda x: x.rect.bottom,
                         reverse=True)
        return choices

    def initialize(self):
        self.titletext = typefaces.prepare_title("Onslaught of Enormities",colour=(255,64,64))
        self.scenery = chromographs.obtain("background.png")
        self.cursor = chromographs.obtain("iconic/unit-cursor.png")
        self.chapter = chapters.open_chapter(self.situation.chapter)
        wave = self.situation.wave
        self.dinosaurs = self.chapter.spawn_wave(wave)
        phonographs.play(self.dinosaurs[-1].attack_phonograph)
        for name in self.chapter.beasts_in_this_chapter():
            if name not in self.situation.seen_dinosaurs:
                self.situation.seen_dinosaurs.append(name)
        self.finished = False
        self.result = "Preparation"
        self.statusbar = gui.StatusBar()
        self.statusbar.push_messages(
            "Protect your ships!",
            "Cannons need soldiers nearby to man them",
            "Click again on the field to direct a soldier",
            "Click on a soldier to select them",
            )
        if self.situation.chapter == 0:
            self.statusbar.flash(80)
        self.situation.update_status_bar(self.statusbar)
        self.selected_unit = None
        # orchestrate the battle music
        phonographs.orchestrate("onslaughtmusic.ogg")

    def render(self):
        self.clear_screen(image=self.scenery)
        self.screen.blit(self.titletext,(10,10))
        self.statusbar.render(self.screen,onslaught=True)

        def render_a_thing(that):
            image = that.image
            position = image.get_rect()
            position.midbottom = that.rect.midbottom
            if that.flash:
                that.flash = False
                image = visual_effects.reddened(image)
            self.screen.blit(image, position)
        # render flat land first
        for land in (land for land in self.situation.installations
                     if land.is_flat):
            render_a_thing(land)
        # render things that lie upon the land
        to_be_drawn = self.situation.installations + self.dinosaurs
        to_be_drawn.sort(key = lambda d: d.rect.bottom)
        debug_rectangles = self.situation.args.debug_rectangles
        # render a wee circle beneath the selected unit
        if self.selected_unit:
            r = self.cursor.get_rect()
            r.center = self.selected_unit.rect.midbottom
            self.screen.blit(self.cursor,r)
        for that in to_be_drawn:
            if that.is_flat:
                continue # already done
            if debug_rectangles:
                pygame.draw.rect(self.screen, (0,255,255), that.rect,1)
                try:
                    pygame.draw.rect(self.screen, (0,255,0), that.rect_of_awareness, 1)
                except AttributeError:
                    pass
                try:
                    pygame.draw.rect(self.screen, (255,200,200), that.rect_of_attack, 1)
                except AttributeError:
                    pass
            render_a_thing(that)
        pygame.display.flip()

    
    def dead_test(self):
        if self.situation.ships_remaining() == 0:
            self.result = "Accounting"
            self.finished = True

    def win_test(self):
        if not any(d for d in self.dinosaurs if not d.destroyed()):
            self.finished = True
            situation = self.situation
            num_waves = len(self.chapter.waves)
            situation.wave += 1
            if situation.wave >= num_waves:
                self.result = "Accounting"

    def move_dinosaurs(self, ms):
        situation = self.situation
        all_the_things = situation.installations + self.dinosaurs
        for d in self.dinosaurs[:]:
            act = d.animate(ms)
            if act:
                targets = d.think(all_the_things)
            if d.finished:
                self.dinosaurs.remove(d)
                all_the_things.remove(d)

    def move_units(self, ms):
        all_the_things = self.situation.installations + self.dinosaurs
        for u in self.situation.installations:
            act = u.animate(ms)
            if not isinstance(u, units.Unit):
                continue
            if act and not u.destroyed():
                targets = u.think(all_the_things)
                if targets:
                    for d in targets:
                        if d.destroyed() or d.exploding:
                            all_the_things.remove(d)
                            self.situation.trophies.append(d.name)

                
