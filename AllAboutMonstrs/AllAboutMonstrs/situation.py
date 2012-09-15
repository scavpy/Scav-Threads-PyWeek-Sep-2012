"""
Here is recorded the current situation of our heroic colony,
an accounting of its wealth and resources, and the attainments
and acquisitions thereof.
"""
from pygame.rect import Rect
from facilities import Fence, Ship, Rock, Puddle, Bush

import os
import sys
import pickle
import random
import grid
from units import Soldier

from math import ceil

SHIP_RECTS = [
    (880,190,128,64),
    (885,260,128,64),
    (840,390,128,64),
    (860,515,128,64),
    ]

class Situation(object):
    maxships = 4
    def __init__(self):
        self.reset("Save")

    def reset(self,name):
        self.savename = name
        self.wealth = 0x1400  # in binary pence
        self.installations = []
        self.reserves = []
        self.population = 5
        self.chapter = 0
        self.wave = 0
        self.progress = 0
        self.seen_dinosaurs = []
        self.death_stats = {}
        self.facility_plans = ["Crops","Housing"]
        self.fence_plans = []
        self.unit_plans = ["Soldier","Sheep"]
        self.last_build = Fence
        self.trophies = []
        self.in_game = False

    def add_installation_if_possible(self, thingclass, location, charge=False):
        thing = thingclass(location)
        collisions = thing.rect.collidelistall(self.installations)
        if collisions:
            obstruance = thing.obstruance
            for i in collisions:
                if obstruance & self.installations[i].exclusion:
                    return False
        if charge:
            self.wealth -= thing.cost
            if thing.human:
                if self.population > 0:
                    self.population -= 1
                    for r in self.reserves:
                        if isinstance(r,thingclass):
                            thing = r
                            thing.rect.center = location.center
                            self.reserves.remove(r)
                else:
                    return False
        self.installations.append(thing)
        self.installations.sort(key=lambda i: i.rect.bottom)

    def land_ho(self):
        plan = grid.TownPlanningOffice()
        for i in range(self.maxships):
            r = SHIP_RECTS[i]
            self.add_installation_if_possible(Ship, Rect(r))
        numscenery = random.randint(0,10)
        scenery = [Rock,Puddle,Bush]
        bounds = grid.BOUNDS
        x,y = bounds.topleft
        for r in range(numscenery):
            px = x+random.randrange(0,bounds.width-100)
            py = y+random.randrange(0,bounds.height)
            lot = plan.nearest_lot(px,py)
            if lot:
                thing = random.choice(scenery)
                self.add_installation_if_possible(thing,lot)
        
    def can_afford_a(self, thing):
        return thing.cost <= self.wealth

    def ships_remaining(self):
        ships = sum([1 for c in self.installations
                  if c.vital and not c.destroyed()])
        return ships

    def get_beasts(self):
        return [b for b in self.installations
                if b.obstruance & grid.obstruance("beast")]

    def get_facilities(self):
        return [f for f in self.installations
                if f.obstruance & grid.obstruance("land","facility","fence")]

    def get_units(self):
        return [u for u in self.installations
                if u.obstruance & grid.obstruance("unit")]

    def count_food(self):
        return sum([max(c.durability-c.damage,0)
                    for c in self.installations
                    if hasattr(c,"edibility")])

    def update_status_bar(self, statusbar):
        food = self.count_food()
        remaining = self.ships_remaining()
        statusbar.update(self.wealth, food, self.population, self.last_build, self.maxships, self.ships_remaining())

    def save_game(self):
        path = os.path.join(self.get_save_dir(),
                            "%s-%d"%(self.savename,self.chapter))
        savefile = open(path,"wb")
        data = self.__dict__
        pickle.dump(data,savefile,protocol=2)
        savefile.close()

    def load_game(self, savefile):
        path = os.path.join(self.get_save_dir(),savefile)
        savefile = open(path,"rb")
        data = pickle.load(savefile)
        self.__dict__.update(data)
        savefile.close()

    def reload_game(self):
        savefile = "%s-%d"%(self.savename,self.chapter)
        self.load_game(savefile)

    def get_save_dir(self):
        savedir = os.path.expanduser("~/.blastosaurusrex")
        if not os.path.exists(savedir):
            os.makedirs(savedir)
        return savedir
