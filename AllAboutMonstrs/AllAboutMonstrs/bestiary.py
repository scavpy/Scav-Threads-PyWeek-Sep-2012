"""
The Bestiary of Animals New to The Arts and Sciences
"""
from pygame.rect import Rect
import units

class Animal(units.Unit):
    """A description of the Animal"""
    notable_attributes = ("Durability","Enormity","Monstrosity")
    name = "Some kind of animal"
    durability = 1
    enormity = 1
    monstrosity = 1
    depiction = "Animal.png"
    footprint = (10,8)

    def __init__(self, location):
        self.damage = 0
        self.rect = Rect(0,0,*self.footprint)
        self.rect.center = location.center
        self.orientation = 2 # o'o'clock
        self.animation_frame = 0
        self.image = self.obtain_frame()
        self.attacking = False
        self.walking = False
        self.temporal_accumulator = 0
        
class Trinitroceratops(Animal):
    """What do these beasts want? To rut and feed and trample with
    abandon. Mere fences are little use against their horns.
    However they are slow to anger and easily pacified with food."""
    name = "Trinitroceratops horridus"
    durability = 50
    enormity = 4
    monstrosity = 5
    depiction = "Trinitroceratops.png"
    animated_chromograph_name = "units/trinitroceratops.png"
    walking_animations = 2
    attacking_animations = 1
    orientation_indices = (1,0,0,0,0,0,1,1,1)

    def __init__(self, location):
        super(Trinitroceratops, self).__init__(location)
