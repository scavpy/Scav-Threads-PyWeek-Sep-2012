"""
Here is recorded the current situation of our heroic colony,
an accounting of its wealth and resources, and the attainments
and acquisitions thereof.
"""

class Situation(object):
    def __init__(self):
        self.wealth = 0  # in binary pence
        self.installations = []

    def add_installation_if_possible(self, thing):
        collision = thing.rect.collidelist(self.installations)
        if collision != -1:
            return False
        self.installations.append(thing)
        self.installations.sort(key=lambda i: i.rect.bottom)
        
