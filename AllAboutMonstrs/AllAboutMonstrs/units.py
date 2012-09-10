"""
  The best defence is an effective means of offence.
"""
from pygame.rect import Rect
import chromographs

class Unit(object):
    notable_attributes = {"Firepower", "Durability", "Manoevrability"}
    walking_animations = 0
    attacking_animations = 0
    orientation_frames = (0,0,0,0,0,0,0,0)

    def obtain_frame(self):
        """ obtain that portion of the animated chromograph
        that shows the unit as standing, walking or attacking
        in its current orientation """
        frames_tall = max(self.orientation_indices) + 1
        frames_wide = self.walking_animations + self.attacking_animations + 1
        anim_row = self.orientation_indices[self.orientation]
        anim_col = self.animation_frame
        return chromographs.obtain_frame(self.animated_chromograph_name,
                                         anim_col, anim_row,
                                         frames_wide, frames_tall)


class Cannon(Unit):
    """ A simple artillery unit """
    name = "Cannon"
    durability = 10
    firepower = 10
    manoevrability = 1
    depiction = "Cannon.png"
    animated_chromograph_name = "units/cannon.png"
    walking_animations = 0
    attacking_animations = 1
    orientation_indices = (0,1,1,1,1,1,0,0,0)

    def __init__(self, location):
        self.damage = 0
        self.rect = Rect(0,0,20,16)
        self.rect.center = location.center
        self.orientation = 6 # o'o'clock
        self.animation_frame = 0
        self.image = self.obtain_frame()

