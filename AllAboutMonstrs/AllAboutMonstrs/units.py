"""
  The best defence is an effective means of offence.
"""
from pygame.rect import Rect
import chromographs

class Cannon(object):
    """ A simple artillery unit """
    notable_attributes = {"Firepower", "Durability", "Manoevrability"}
    name = "Cannon"
    durability = 10
    firepower = 10
    manoevrability = 1
    depiction = "Cannon.png"

    def __init__(self, location):
        self.damage = 0
        self.orientation = "L"
        self.rect = Rect(0,0,20,16)
        self.rect.center = location.center
        self.condition = 0
        self.image = chromographs.obtain("iconic/cannon.png")
