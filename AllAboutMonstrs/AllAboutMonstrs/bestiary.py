"""
The Bestiary of Animals New to The Arts and Sciences
"""
from pygame.rect import Rect
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

    def __init__(self, location):
        self.damage = 0
        self.rect = Rect(0,0,*self.footprint)
        self.rect.center = location.center
        self.animation_frame = 0
        self.orient(2)
        self.image = self.obtain_frame()
        self.attacking = False
        self.walking = False
        self.temporal_accumulator = 0
        self.directions = Rect(0,0,self.velocity, round(self.velocity * 0.8))
        self.directions.center = (0,0)

    def orient(self, orientation):
        """ arrange the areas of awareness and attack
        depending on the orientation as a number on
        the octoclock.
           0
         7   1
        6     2
         5   3
           4
        """
        self.orientation = orientation
        centre_of_attention = octoclock_direction(self.rect, orientation)
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
    velocity = 3
    monstrosity = 1
    depiction = "Trinitroceratops.png"
    animated_chromograph_name = "units/trinitroceratops.png"
    walking_animations = 2
    attacking_animations = 1
    orientation_indices = (1,0,0,0,0,0,1,1,1)
    footprint = (50,40)
    area_of_awareness = (100,80)
    area_of_attack = (25,20)

    def __init__(self, location):
        super(Trinitroceratops, self).__init__(location)
        self.bored = False
        self.angry = False
        self.satiety = 0

    def think(self, things):
        """ Determine the volition of the beast,
        return a true value if it moved """
        indices = self.rect_of_awareness.collidelistall(things)
        knowledge = [things[i] for i in indices]
        food = [] # crops in knowledge
        vector = octoclock_direction(self.directions, self.orientation)
        next_position = self.rect.move(vector)
        indices = next_position.collidelistall(knowledge)
        obstacles = [things[i] for i in indices
                     if things[i] is not self]
        if not obstacles and grid.BOUNDS.contains(next_position):
            self.rect = next_position
            return True
        if next_position.right >= grid.BOUNDS.right:
            self.bored = True
            self.orient(6) # go back
            return False
        if self.bored and next_position.left < 0:
            self.rect = next_position
            if next_position.right < 0:
                self.dead = True
            return True
        
