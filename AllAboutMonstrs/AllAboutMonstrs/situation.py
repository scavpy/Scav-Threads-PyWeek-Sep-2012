"""
Here is recorded the current situation of our heroic colony,
an accounting of its wealth and resources, and the attainments
and acquisitions thereof.
"""

from facilities import Fence

class Situation(object):
    def __init__(self):
        self.wealth = 2560  # in binary pence
        self.installations = []
        self.population = 5
        self.chapter = 0
        self.wave = 0
        self.seen_dinosaurs = []
        self.facility_plans = ["Crops"]
        self.fence_plans = ["Fence"]
        self.unit_plans = ["Cannon"]
        self.last_fence_build = Fence
        self.last_lot_build = None

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
