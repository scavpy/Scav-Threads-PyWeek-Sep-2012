"""
  The best defence is an effective means of offence.
"""
from pygame.rect import Rect
import random
import chromographs
import grid


def octoclock_direction(ooclock, rect):
    return getattr(rect, ("midtop","topright","midright","bottomright",
                          "midbottom","bottomleft","midleft","topleft")[ooclock])

class Unit(object):
    notable_attributes = {"Firepower", "Durability", "Velocity"}
    walking_animations = 0
    attacking_animations = 0
    orientation_frames = (0,0,0,0,0,0,0,0)
    pace = 100
    footprint = (10,8)
    area_of_awareness = (50,40)
    area_of_attack = (10, 8)
    obstruance = grid.obstruance("notland")
    is_flat = False

    def __init__(self, location):
        self.damage = 0
        self.rect = Rect(0,0,*self.footprint)
        self.rect.center = Rect(location).center
        self.animation_frame = 0
        self.orient(6)
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
            return False # nothing to be done
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
        return True # something was changed

class Cannon(Unit):
    """ A simple artillery unit """
    name = "Cannon"
    durability = 10
    firepower = 10
    velocity = 2
    depiction = "Cannon.png"
    animated_chromograph_name = "units/cannon.png"
    walking_animations = 0
    attacking_animations = 2
    orientation_indices = (0,1,1,1,1,1,0,0,0)
    footprint = 20,16
    area_of_awareness = (100,80)
    area_of_attack = (90, 75)

    def __init__(self, location):
        super(Cannon, self).__init__(location)

    def think(self, things):
        """ Determine the tactics of the unit """
        # just fire randomly
        if random.random < 0.01:
            self.attack()
