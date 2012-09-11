"""
The Bestiary of Animals New to The Arts and Sciences
"""
from pygame.rect import Rect
import random
import units
import grid

class Animal(units.Unit):
    """A description of the Animal"""
    notable_attributes = ("Durability","Voracity","Monstrosity",
                          "Velocity","Destructiveness")
    name = "Some kind of animal"
    durability = 1
    voracity = 1
    velocity = 1
    monstrosity = 1
    destructiveness = 1
    rapidity = 1 # for animals, rapidity should maybe equal velocity
    depiction = "Animal.png"
    obstruance = grid.obstruance("beast")
    exclusion = grid.obstruance("notland")

    def attend_to_attack_area(self, centre):
        """ Beasts have close-in attacks """
        self.rect_of_attack.center = centre


class Trinitroceratops(Animal):
    """What do these beasts want? To rut and feed and trample with
    abandon. Mere fences are little use against their horns.
    However they are slow to anger and easily pacified with food."""
    name = "Trinitroceratops horridus"
    durability = 50
    voracity = 4
    velocity = 5
    rapidity = 5
    monstrosity = 1
    destructiveness = 8
    depiction = "Trinitroceratops.png"
    animated_chromograph_name = "units/trinitroceratops.png"
    walking_animations = 2
    attacking_animations = 1
    orientation_indices = (1,0,0,0,0,0,1,1,1)
    footprint = (45,20)
    area_of_awareness = (100,80)
    area_of_attack = (30,24)

    def __init__(self, location):
        super(Trinitroceratops, self).__init__(location)
        self.orient(2)
        self.bored = False
        self.angry = False
        self.satiety = 0
        self.walking = True

    def think(self, things):
        """ Determine the volition of the beast.
        If it acted upon any thing else, return a list of such
        things. Otherwise return a non-true value.
        """
        indices = self.rect_of_awareness.collidelistall(things)
        knowledge = [things[i] for i in indices]
        food = [] # crops in knowledge
        if self.walking:
            vector = units.octoclock_direction(self.orientation, self.directions)
            next_position = self.rect.move(vector)
        else:
            next_position = self.rect
        indices = next_position.collidelistall(knowledge)
        obstacles = [knowledge[i] for i in indices
                     if knowledge[i] is not self]
        if obstacles:
            indices = self.rect_of_attack.collidelistall(obstacles)
            if indices:
                targets = [obstacles[i] for i in indices 
                           if not isinstance(obstacles[i], Animal)]
                if targets and not self.attacking:
                    target = targets[0]
                    self.attack()
                    target.harm(self.destructiveness)
                    return [target]
            directions = (0,1,2,3,4,5,6,7) + ((4,5,6) if self.bored else (1,2,3))
            self.orient(random.choice(directions))
            return
        bounds = grid.BOUNDS
        if bounds.contains(next_position):
            self.move(next_position)
            return
        if next_position.right >= bounds.right:
            self.bored = True
            self.orient(6) # go back
            return
        if next_position.left <= 0:
            self.move(next_position)
            if self.bored:
                if next_position.right < 0:
                    self.finished = True
            else:
                self.orient(random.randint(1,3))
            return
        if next_position.top < bounds.top:
            self.orient(5 if self.bored else 3)
            return
        if next_position.bottom >= bounds.bottom:
            self.orient(7 if self.bored else 1)
            return
        print "WTF!", id(self), "is stuck for no known reason"

