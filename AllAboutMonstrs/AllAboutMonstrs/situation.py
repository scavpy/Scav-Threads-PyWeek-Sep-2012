"""
Here is recorded the current situation of our heroic colony,
an accounting of its wealth and resources, and the attainments
and acquisitions thereof.
"""

class Situation(object):
    def __init__(self):
        self.wealth = 0  # in binary pence
        self.installations = []
        self.chapter = 0
        self.wave = 0
        self.seen_dinosaurs = []

    def add_installation_if_possible(self, thing):
        collisions = thing.rect.collidelistall(self.installations)
        if collisions:
            obstruance = thing.obstruance
            for i in collisions:
                if obstruance & self.installations[i].exclusion:
                    return False
        self.installations.append(thing)
        self.installations.sort(key=lambda i: i.rect.bottom)
        
