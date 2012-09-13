"""
 Facilities and fences
"""

from pygame.rect import Rect
import chromographs
import grid


class Facility(object):
    notable_attributes = {"Durability","Flammability","Habitability"}
    standing_animations = 1
    cost = 0x100
    conditions = 4 # good, serviceable, dilapidated, ruined
    pace = 1000
    obstruance = grid.obstruance("all")
    is_flat = False # flat things drawn first
    aliment = None
    vital = False

    def __init__(self, location):
        self.damage = 0
        self.animation_frame = 0
        self.temporal_accumulator = 0
        self.condition = 0
        self.rect = Rect(0,0, *self.footprint)
        self.rect.center = location.center
        self.image = self.obtain_frame()
        self.flash = False

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

    def harm(self, quanta_of_destruction):
        """ damage the structure, worsening its condition
        accordingly """
        self.damage += quanta_of_destruction
        self.flash = True
        damage = self.damage
        ruination = self.durability
        if damage == 0:
            self.condition = 0
        elif damage >= ruination:
            self.condition = self.conditions - 1
            self.obstruance = 0 # effectively no longer present
        else:
            self.condition = max((damage * self.conditions) // ruination, 1)
        self.image = self.obtain_frame()

    def destroyed(self):
        return self.damage >= self.durability

class Fence(Facility):
    name = "Wooden Fence"
    durability = 10
    flammability = 2
    habitability = 0
    pace = 1000
    cost = 0x050

    def __init__(self, location):
        self.damage = 0
        self.animation_frame = 0
        self.temporal_accumulator = 0
        self.condition = 0
        horizontal = (location.width/location.height) > 1
        direction = "hfence" if horizontal else "vfence"
        self.animated_chromograph_name = "facilities/%s.png"%direction
        self.footprint = ((grid.LOT_WIDTH, 2 * grid.FENCE_MARGIN_NORTH)
                     if horizontal else
                     (2 * grid.FENCE_MARGIN_WEST, grid.LOT_DEPTH))
        self.obstruance = grid.obstruance(direction)
        self.exclusion = grid.obstruance(direction,"beast","unit","facility")
        self.rect = Rect(0,0, *self.footprint)
        self.rect.center = location.center
        self.image = self.obtain_frame()
        self.flash = False


class Crops(Facility):
    name = "Cabbages"
    is_flat = True
    notable_attributes = {"Edibility","Flammability","Habitability"}
    edibility = 9
    durability = 9
    flammability = 1
    habitability = 0
    placement_phonograph = "dig.ogg"
    animated_chromograph_name = "facilities/crops.png"
    obstruance = grid.obstruance("land")
    exclusion = grid.obstruance("beast","unit","facility","land")
    footprint = (grid.LOT_WIDTH, grid.LOT_DEPTH)
    cost = 0x028
    aliment = "Vegetable"

class Housing(Facility):
    name = "Housing"
    durability = 40
    animated_chromograph_name = "facilities/housing.png"
    standing_animations = 4
    obstruance = grid.obstruance("facility")
    exclusion = grid.obstruance("notland")
    footprint = (grid.LOT_WIDTH-10, grid.LOT_DEPTH-8)
    cost = 0x300
    pace = 200

class Ship(Facility):
    vital = True
    durability = 1000
    animated_chromograph_name = "facilities/ship.png"
    standing_animations = 1
    conditions = 4
    obstruance = grid.obstruance("facility")
    exclusion = grid.obstruance("notland")
    footprint = (128,40)
