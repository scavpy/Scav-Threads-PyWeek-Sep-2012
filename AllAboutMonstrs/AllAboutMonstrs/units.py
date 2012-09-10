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
    pace = 100

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
    def attack(self):
        """ Assume a ferocius aspect """
        if self.attacking or not self.attacking_animations:
            return
        self.temporal_accumulator = 0
        self.attacking = True
        self.animation_frame = self.walking_animations + 1
        self.image = self.obtain_frame()

    def animate(self, ms):
        """ Create the illusion of movement """
        self.temporal_accumulator += ms
        if self.temporal_accumulator < self.pace:
            return
        self.temporal_accumulator = 0
        frame = self.animation_frame
        if self.walking:
            frame += 1
            if frame > self.walking_animations:
                frame = 1
        elif self.attacking:
            frame += 1
            if frame > self.walking_animations + self.attacking_animations:
                frame = 0
                self.attacking = False
        else:
            assert frame == 0
        self.animation_frame = frame
        self.image = self.obtain_frame()

class Cannon(Unit):
    """ A simple artillery unit """
    name = "Cannon"
    durability = 10
    firepower = 10
    manoevrability = 1
    depiction = "Cannon.png"
    animated_chromograph_name = "units/cannon.png"
    walking_animations = 0
    attacking_animations = 2
    orientation_indices = (0,1,1,1,1,1,0,0,0)

    def __init__(self, location):
        self.damage = 0
        self.rect = Rect(0,0,20,16)
        self.rect.center = location.center
        self.orientation = 6 # o'o'clock
        self.animation_frame = 0
        self.image = self.obtain_frame()
        self.attacking = False
        self.walking = False
        self.temporal_accumulator = 0
