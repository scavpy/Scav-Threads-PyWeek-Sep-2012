"""
The Bestiary of Animals New to The Arts and Sciences
"""
from pygame.rect import Rect
import random
import units
import grid

def octoclock_direction(ooclock, rect):
    return getattr(rect, ("midtop","topright","midright","bottomright",
                          "midbottom","bottomleft","midleft","topleft")[ooclock])

class Animal(units.Unit):
    """A description of the Animal"""
    notable_attributes = ("Durability","Voracity","Monstrosity",
                          "Velocity")
    name = "Some kind of animal"
    durability = 1
    voracity = 1
    velocity = 1
    monstrosity = 1
    depiction = "Animal.png"
    footprint = (10,8)
    area_of_awareness = (50,40)
    area_of_attack = (10, 8)
    obstruance = grid.obstruance("all")

    def __init__(self, location):
        self.damage = 0
        self.rect = Rect(0,0,*self.footprint)
        self.rect.center = location[:2]
        self.animation_frame = 0
        self.orient(2)
        self.image = self.obtain_frame()
        self.attacking = False
        self.walking = False
        self.finished = False
        self.temporal_accumulator = 0
        self.directions = Rect(0,0,self.velocity, round(self.velocity * 0.8))
        self.directions.center = (0,0)

    def orient(self, orientation):
        self.orientation = orientation
        self.attend_to_surroundings()

    def move(self, location):
        self.rect = location
        self.attend_to_surroundings()

    def attend_to_surroundings(self):
        """ arrange the areas of awareness and attack
        depending on the orientation as a number on
        the octoclock.
           0
         7   1
        6     2
         5   3
           4
        """
        centre_of_attention = octoclock_direction(self.orientation, self.rect)
        self.rect_of_awareness = Rect(0,0,*self.area_of_awareness)
        self.rect_of_awareness.center = centre_of_attention
        self.rect_of_attack = Rect(0,0,*self.area_of_attack)
        self.rect_of_attack.center = centre_of_attention

class Trinitroceratops(Animal):
    """What do these beasts want? To rut and feed and trample with
    abandon. Mere fences are little use against their horns.
    However they are slow to anger and easily pacified with food."""
    name = "Trinitroceratops horridus"
    durability = 50
    voracity = 4
    velocity = 5
    monstrosity = 1
    depiction = "Trinitroceratops.png"
    animated_chromograph_name = "units/trinitroceratops.png"
    walking_animations = 2
    attacking_animations = 1
    orientation_indices = (1,0,0,0,0,0,1,1,1)
    footprint = (45,20)
    area_of_awareness = (100,80)
    area_of_attack = (20,16)

    def __init__(self, location):
        super(Trinitroceratops, self).__init__(location)
        self.bored = False
        self.angry = False
        self.satiety = 0
        self.walking = True

    def think(self, things):
        """ Determine the volition of the beast,
        return a true value if it moved """
        indices = self.rect_of_awareness.collidelistall(things)
        knowledge = [things[i] for i in indices]
        food = [] # crops in knowledge
        if self.walking:
            vector = octoclock_direction(self.orientation, self.directions)
            next_position = self.rect.move(vector)
        else:
            next_position = self.rect
        indices = next_position.collidelistall(knowledge)
        obstacles = [knowledge[i] for i in indices
                     if knowledge[i] is not self]
        if obstacles:
            directions = (0,1,2,3,4,5,6,7) + ((4,5,6) if self.bored else (1,2,3))
            self.orient(random.choice(directions))
            return False
        bounds = grid.BOUNDS
        if bounds.contains(next_position):
            self.move(next_position)
            return True
        if next_position.right >= bounds.right:
            self.bored = True
            self.orient(6) # go back
            return False
        if next_position.left <= 0:
            self.move(next_position)
            if self.bored:
                if next_position.right < 0:
                    self.finished = True
            else:
                self.orient(random.randint(1,3))
            return True
        if next_position.top < bounds.top:
            self.orient(5 if self.bored else 3)
            return False
        if next_position.bottom >= bounds.bottom:
            self.orient(7 if self.bored else 1)
            return False
        print "WTF!", id(self), "is stuck for no known reason"

