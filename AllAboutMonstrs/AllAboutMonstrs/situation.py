"""
Here is recorded the current situation of our heroic colony,
an accounting of its wealth and resources, and the attainments
and acquisitions thereof.
"""

from facilities import Fence

import os
import sys
import pickle

class Situation(object):
    def __init__(self):
        self.savename = "Save"
        self.wealth = 0x2000  # in binary pence
        self.installations = []
        self.population = 5
        self.chapter = 0
        self.wave = 0
        self.progress = 0
        self.seen_dinosaurs = []
        self.facility_plans = ["Crops","Housing"]
        self.fence_plans = ["Fence"]
        self.unit_plans = ["Cannon"]
        self.last_fence_build = Fence
        self.last_lot_build = None
        self.trophies = []

    def add_installation_if_possible(self, thing, charge=False):
        collisions = thing.rect.collidelistall(self.installations)
        if collisions:
            obstruance = thing.obstruance
            for i in collisions:
                if obstruance & self.installations[i].exclusion:
                    return False
        if charge:
            self.wealth -= thing.cost
        self.installations.append(thing)
        self.installations.sort(key=lambda i: i.rect.bottom)
        
    def can_afford_a(self, thing):
        return thing.cost <= self.wealth

    def update_status_bar(self, statusbar):
        food = sum([max(c.durability - c.damage, 0)
                    for c in self.installations if hasattr(c,"edibility")])
        statusbar.update(self.wealth, food)

    def save_game(self):
        path = os.path.join(self.get_save_dir(),
                            "%s-%d"%(self.savename,self.chapter))
        savefile = open(path,"w")
        data = self.__dict__
        pickle.dump(data,savefile,protocol=2)
        savefile.close()

    def load_game(self, savefile):
        path = os.path.join(self.get_save_dir(),savefile)
        savefile = open(path,"r")
        data = pickle.load(savefile)
        self.__dict__.update(data)
        savefile.close()

    def get_save_dir(self):
        savedir = os.path.expanduser("~/.blastosaurusrex")
        if not os.path.exists(savedir):
            os.makedirs(savedir)
        return savedir
