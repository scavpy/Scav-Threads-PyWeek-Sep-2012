"""
 Facilities and fences
"""

from pygame.rect import Rect
import chromographs
import grid


class Facility(object):
    notable_attributes = {"Durability","Flammability","Habitability"}
    standing_animations = 1
    conditions = 4 # good, serviceable, dilapidated, ruined
    pace = 100
    obstruance = grid.obstruance("all")

    def obtain_frame(self):
        """ obtain that portion of the animated chromograph
        that shows the facility in its current condition """
        frames_tall = self.conditions
        frames_wide = self.standing_animations
        anim_row = self.condition
        anim_col = self.animation_frame
        return chromographs.obtain_frame(self.animated_chromograph_name,
                                         anim_col, anim_row,
                                         frames_wide, frames_tall)

    def animate(self, ms):
        """ Create the illusion of movement """
        self.temporal_accumulator += ms
        if self.temporal_accumulator < self.pace:
            return False # nothing to be done
        self.temporal_accumulator = 0
        frame = self.animation_frame
        if self.standing_animations > 1:
            frame = (frame + 1) % self.standing_animations
        else:
            frame = 0
        self.animation_frame = frame
        self.image = self.obtain_frame()
        return True # something was changed

    def damage(self, quanta_of_destruction):
        """ damage the structure, worsening its condition
        accordingly """
        self.damage += quanta_of_destruction
        damage = self.damage
        ruination = self.durability
        if damage == 0:
            self.condition = 0
        elif damage >= ruination:
            self.condition = self.conditions - 1
        else:
            self.condition = max((ruination * self.conditions) // damage, 1)
        self.image = self.obtain_frame()

class AbstractFence(Facility):
    durability = 5
    flammability = 5
    habitability = 0
    pace = 1000

    def __init__(self, location):
        self.damage = 0
        self.animaton_frame = 0
        self.temporal_accumulator = 0
        self.condition = 0
        self.rect = Rect(0,0, *self.footprint)
        self.rect.center = location.center

class HorizontalFence(Abstractfence):
    animated_chromograph_name = "facilities/hfence.png"
    footprint = (grid.LOT_WIDTH, 2 * grid.FENCE_MARGIN_NORTH)
    obstruance = grid.obstruance("hfence","beast","unit","facility")

class VerticalFence(Abstractfence):
    animated_chromograph_name = "facilities/vfence.png"
    footprint = (2 * grid.FENCE_MARGIN_WEST, grid.LOT_DEPTH)
    obstruance = grid.obstruance("vfence","beast","unit","facility")

