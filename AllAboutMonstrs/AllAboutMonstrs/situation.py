"""
Here is recorded the current situation of our heroic colony,
an accounting of its wealth and resources, and the attainments
and acquisitions thereof.
"""

class Situation(object):
    def __init__(self):
        self.wealth = 0  # in binary pence
        self.installations = []
        self.facility_plans = ["Crops"]
        self.unit_plans = ["Cannon"]
        self.most_recent_build = None

    def add_installation_if_possible(self, thing):
        collisions = thing.rect.collidelistall(self.installations)
        if collisions:
            obstruance = thing.obstruance
            for i in collisions:
                if obstruance & self.installations[i].exclusion:
                    return False
        self.installations.append(thing)
        self.installations.sort(key=lambda i: i.rect.bottom)
        
