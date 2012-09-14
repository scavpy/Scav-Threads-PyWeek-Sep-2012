"""
 Facilities and fences
"""

from pygame.rect import Rect
import chromographs
import phonographs
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
    human = False

    def __init__(self, location):
        self.damage = 0
        self.animation_frame = 0
        self.temporal_accumulator = 0
        self.condition = 0
        self.rect = Rect(0,0, *self.footprint)
        self.rect.center = location.center
        self.image = self.obtain_frame()
        self.flash = False

    def __getstate__(self):
        state = self.__dict__.copy()
        state["image"] = None
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.image = self.obtain_frame()

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

    def repair(self):
        self.damage = 0
        self.condition = 0
        self.image = self.obtain_frame()
        phonographs.play("cannon-place.ogg")

    def destroyed(self):
        return self.damage >= self.durability

class Fence(Facility):
    name = "Wooden Fence"
    chromograph_suffix = "fence"
    placement_phonograph = "crack.ogg"
    durability = 40
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
        direction = "h" if horizontal else "v"
        self.animated_chromograph_name = "facilities/%s.png"%(direction+self.chromograph_suffix)
        self.footprint = ((grid.LOT_WIDTH, 2 * grid.FENCE_MARGIN_NORTH)
                     if horizontal else
                     (2 * grid.FENCE_MARGIN_WEST, grid.LOT_DEPTH))
        self.obstruance = grid.obstruance(direction+"fence")
        self.exclusion = grid.obstruance(direction+"fence","beast","unit","facility")
        self.rect = Rect(0,0, *self.footprint)
        self.rect.center = location.center
        self.image = self.obtain_frame()
        self.flash = False

class Wall(Fence):
    name = "Brick Wall"
    chromograph_suffix = "wall"
    durability = 100
    flammability = 0
    cost = 0x100
    placement_phonograph = "brick.ogg"

class Crops(Facility):
    name = "Cabbages"
    is_flat = True
    notable_attributes = {"Edibility","Flammability","Habitability"}
    edibility = 12
    durability = 12
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
    durability = 120
    habitability = 3
    animated_chromograph_name = "facilities/housing.png"
    standing_animations = 4
    obstruance = grid.obstruance("facility")
    exclusion = grid.obstruance("all")
    footprint = (grid.LOT_WIDTH-10, grid.LOT_DEPTH-8)
    cost = 0x300
    pace = 200
    placement_phonograph = "brick.ogg"

class Ship(Facility):
    name = "Ship"
    vital = True
    durability = 1000
    habitability = 1
    animated_chromograph_name = "facilities/ship.png"
    standing_animations = 1
    conditions = 4
    obstruance = grid.obstruance("facility")
    exclusion = grid.obstruance("all")
    footprint = (128,40)
    cost = 0xa00
