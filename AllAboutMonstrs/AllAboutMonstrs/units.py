"""
  The best defence is an effective means of offence.
"""
from time import time
from pygame.rect import Rect
import random
import phonographs
import chromographs
import grid
from math import sqrt, atan2, pi

def octoclock_direction(ooclock, rect):
    return getattr(rect, ("midtop","topright","midright","bottomright",
                          "midbottom","bottomleft","midleft","topleft")[ooclock])

def place_opposite(rect, ooclock, position):
    """ place a rectangle so that it touches the given position
    on its opposite side or corner to the given octoclock direction """
    attr = ("midbottom","bottomleft","midleft","topleft",
            "midtop","topright","midright","bottomright")[ooclock]
    setattr(rect, attr, position)


class Unit(object):
    notable_attributes = {"Firepower", "Durability", "Velocity","Rapidity"}
    walking_animations = 0
    attacking_animations = 0
    orientation_frames = (0,0,0,0,0,0,0,0)
    cost = 2560
    pace = 100
    obstruance = grid.obstruance("unit")
    exclusion = grid.obstruance("notland")
    footprint = (10,8)
    area_of_awareness = (50,40)
    area_of_attack = (10, 8)
    is_flat = False
    aliment = None

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
        self.reload_time = 0

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
        self.attend_to_attack_area(centre_of_attention)

    def attend_to_attack_area(self, centre):
        """ Our modern military units have ranged attacks """
        place_opposite(self.rect_of_attack, self.orientation, centre)

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
        if self.reload_time > time():
            return
        self.temporal_accumulator = 0
        self.attacking = True
        self.reload_time = time() + 5.0 / self.rapidity
        self.animation_frame = self.walking_animations + 1
        self.image = self.obtain_frame()
        return True

    def animate(self, ms):
        """ Create the illusion of movement """
        self.temporal_accumulator += ms
        if self.temporal_accumulator < self.pace:
            return False # nothing to be done
        self.temporal_accumulator = 0
        frame = self.animation_frame
        if self.attacking:
            frame += 1
            if frame > self.walking_animations + self.attacking_animations:
                print self.name, "finished attack"
                frame = 0
                self.attacking = False
            else:
                print self.name, "attack frame", frame
        elif self.walking:
            frame += 1
            if frame > self.walking_animations:
                frame = 1
        else:
            assert frame == 0
        self.animation_frame = frame
        self.image = self.obtain_frame()
        return True # something was changed

    def harm(self, quanta_of_destruction):
        """ Deal damage to the unit, possibly rendering it inactive """
        self.damage += quanta_of_destruction
        if self.damage > self.durability:
            self.rect.width = 0
            self.rect.height = 0

    def destroyed(self):
        return self.damage >= self.durability

    def things_perceived(self, things):
        """ things that are perceived """
        indices = self.rect_of_awareness.collidelistall(things)
        return [things[i] for i in indices]

    def things_in_range(self, things):
        indices = self.rect_of_attack.collidelistall(things)

    def find_obstacles(self, location, knowledge):
        """ find things that obstruct a rectangle such that this
        unit may not occupy the same space if it were there """
        indices = location.collidelistall(knowledge)
        return [knowledge[i] for i in indices
                if knowledge[i] is not self
                and (knowledge[i].obstruance & self.exclusion)]

    def find_nearest(self, things):
        """ nearest thing sorted by distance from centre """
        def dist(thing):
            rx, ry = thing.rect.center
            mx, my = self.rect.center
            return sqrt((rx - mx)**2 + (ry - my)**2)
        return sorted(things, key=dist)

    def orientation_towards(self, position):
        """ octaclock direction from self centre to position """
        cx, cy = self.rect.center
        px, py = position[:2]
        dx = px - cx
        dy = py - cy
        steep = (dx == 0) or abs(dy / dx) > 3
        shallow = (dy == 0) or abs(dx / dy) > 3
        if steep:
            return 0 if dy < 0 else 4
        if shallow:
            return 2 if dx > 0 else 6
        if dy < 0:
            return 1 if dx > 0 else 7
        return 3 if dx > 0 else 5
        
        
class Cannon(Unit):
    """ A simple artillery unit """
    name = "Cannon"
    durability = 10
    firepower = 10
    velocity = 2
    rapidity = 1
    depiction = "Cannon.png"
    placement_phonograph = "cannon-place.ogg"
    animated_chromograph_name = "units/cannon.png"
    walking_animations = 0
    attacking_animations = 2
    orientation_indices = (0,1,1,1,1,1,0,0,0)
    footprint = 20,16
    area_of_awareness = (200,160)
    area_of_attack = (80, 64)
    pace = 100
    cost = 512

    def __init__(self, location):
        super(Cannon, self).__init__(location)
        reload_time = 0

    def think(self, things):
        """ Determine the tactics of the unit.
        If it acted upon any thing else, return a list of such
        things. Otherwise return a non-true value.
        """
        # Fire when any beast is attackable
        from bestiary import Animal
        indices = self.rect_of_attack.collidelistall(things)
        beasts = [things[i] for i in indices
                  if isinstance(things[i], Animal)]
        if beasts and not self.attacking:
            target = beasts[0] # TODO pick closest?
            if self.attack():
                target.harm(self.firepower)
                phonographs.play("cannon.ogg")
                return [target]


