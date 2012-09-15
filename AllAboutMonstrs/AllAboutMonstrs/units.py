"""
  The best defence is an effective means of offence.
"""
from time import time
from pygame.rect import Rect
import random
import phonographs
import chromographs
import grid

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
    cost = 0xa00
    pace = 50
    obstruance = grid.obstruance("unit")
    exclusion = grid.obstruance("notland")
    footprint = (10,8)
    area_of_awareness = (50,40)
    area_of_attack = (10, 8)
    is_flat = False
    aliment = None
    vital = False
    destination = None
    human = False

    def __init__(self, location):
        self.damage = 0
        self.rect = Rect(0,0,*self.footprint)
        self.rect.center = Rect(location).center
        self.animation_frame = 1
        self.orient(6)
        self.image = self.obtain_frame()
        self.attacking = False
        self.walking = False
        self.finished = False
        self.temporal_accumulator = random.randint(0,20)
        self.directions = Rect(0,0,self.velocity, round(self.velocity * 0.8))
        self.directions.center = (0,0)
        self.reload_time = 0
        self.flash = False
        self.killed_by = None

    def __getstate__(self):
        state = self.__dict__.copy()
        state["image"] = None
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.image = self.obtain_frame()

    
    def step_position(self):
        """ where will it be on the next step? """
        if self.walking:
            vector = octoclock_direction(self.orientation, self.directions)
            next_position = self.rect.move(vector)
        else:
            next_position = self.rect
        return next_position

    def orient(self, orientation):
        self.orientation = orientation
        self.attend_to_surroundings()

    def navigate(self, next_position):
        if grid.rect_in_bounds(next_position):
            self.move(next_position)

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
        phonographs.play(self.attack_phonograph)
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
                frame = 1
                self.attacking = False
        elif self.walking:
            frame += 1
            if frame > self.walking_animations:
                frame = 1

        self.animation_frame = frame
        self.image = self.obtain_frame()
        return True # something was changed

    def harm(self, quanta_of_destruction, cause=None):
        """ Deal damage to the unit, possibly rendering it inactive """
        self.damage += quanta_of_destruction
        self.flash = True
        if self.damage >= self.durability:
            self.obstruance = 0
            self.animation_frame = 0
            self.walking = False
            self.attacking = False
            self.image = self.obtain_frame()
            self.killed_by = cause

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
            return (rx - mx)**2 + (ry - my)**2
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
    """ A simple artillery unit. Powerful, but useless without
    good soldiers to man it."""
    name = "Cannon"
    durability = 15
    firepower = 10
    velocity = 0
    rapidity = 1
    depiction = "Cannon.png"
    placement_phonograph = "cannon-place.ogg"
    animated_chromograph_name = "units/cannon.png"
    walking_animations = 1
    attacking_animations = 2
    orientation_indices = (2,1,1,1,3,0,0,0)
    footprint = 20,16
    area_of_awareness = (200,160)
    area_of_attack = (80, 64)
    attack_phonograph = "cannon.ogg"
    pace = 100
    cost = 0x180

    def think(self, things):
        """ Determine the tactics of the unit.
        If it acted upon any thing else, return a list of such
        things. Otherwise return a non-true value.
        """
        # Fire when any beast is attackable
        from bestiary import Animal
        indices = self.rect_of_awareness.collidelistall(things)
        category = grid.obstruance("beast")
        beasts = self.find_nearest([things[i] for i in indices
                                    if things[i].obstruance & category])
        crew = self.find_nearest([things[i] for i in indices
                                   if things[i].human and not things[i].destroyed()])
        if beasts and not self.attacking and crew:
            target = beasts[0]
            self.orient(self.orientation_towards(target.rect.center))
            if self.rect_of_attack.colliderect(target.rect):
                if self.attack():
                    target.harm(self.firepower, "gunfire")
                    return [target]

class AnalyticalCannon(Unit):
    """ A cannon operated by analytical engine, aimed using
    a directional seismonstrograph. Fires rapidly and
    accurately without a gun crew."""
    name = "Analytical Cannon"
    durability = 15
    firepower = 5
    velocity = 0
    rapidity = 5
    depiction = "AnalyticalCannon.png"
    placement_phonograph = "cannon-place.ogg"
    animated_chromograph_name = "units/analyticalcannon.png"
    walking_animations = 1
    attacking_animations = 2
    orientation_indices = (2,1,1,1,3,0,0,0)
    footprint = 20,16
    area_of_awareness = (200,160)
    area_of_attack = (80, 64)
    attack_phonograph = "cannon.ogg"
    pace = 100
    cost = 0x400

    def think(self, things):
        """ Determine the tactics of the unit.
        If it acted upon any thing else, return a list of such
        things. Otherwise return a non-true value.
        """
        # Fire when any beast is attackable
        from bestiary import Animal
        indices = self.rect_of_awareness.collidelistall(things)
        beasts = self.find_nearest([things[i] for i in indices
                                    if isinstance(things[i], Animal)])
        if beasts and not self.attacking:
            target = beasts[0]
            self.orient(self.orientation_towards(target.rect.center))
            if self.rect_of_attack.colliderect(target.rect):
                if self.attack():
                    target.harm(self.firepower, "gunfire")
                    return [target]

class Soldier(Unit):
    """ An infantry unit. """
    name = "Soldier"
    durability = 10
    firepower = 2
    velocity = 7
    rapidity = 3
    animated_chromograph_name = "units/soldier.png"
    walking_animations = 2
    attacking_animations = 2
    orientation_indices = (1,1,1,1,0,0,0,0)
    footprint = (10,10)
    area_of_awareness = (200,160)
    area_of_attack = (100,80)
    attack_phonograph = "rifle.ogg"
    pace = 50
    cost = 0x000
    aliment = "Meat"
    human = True
    ranks = ["Pt", "Cpl", "Sgt", "Lt", "Capt", "Maj", "Col", "Brig", "Gen"]

    soldier_names = """Adam Alan Bob Bill Bert Bryn Chas Dai Dave Dick Dan Dara
        Ed Edd Eddy Fred Greg Hal Herb John Jim Jas Jack Jock Joe
        Leo Len Mo Olly Pete Paul Rob Rick Stan Sam Tom Will Zach Zeb
        """.split()
    random.shuffle(soldier_names)
    next_name = 0

    def __init__(self, location):
        super(Soldier, self).__init__(location)
        self.name = Soldier.soldier_names[Soldier.next_name]
        Soldier.next_name = (Soldier.next_name + 1) % len(Soldier.soldier_names)
        self.rank = 0

    def think(self, things):
        indices = self.rect_of_awareness.collidelistall(things)
        beasts = self.find_nearest([things[i] for i in indices
                                    if things[i].obstruance &
                                    grid.obstruance("beast")])
        if self.destination:
            self.walking = True
            self.orient(self.orientation_towards(self.destination))
            self.navigate(self.step_position())
            if self.rect.collidepoint(self.destination):
                self.destination = None
                self.walking = False
        if beasts and not self.attacking:
            target = beasts[0]
            self.orient(self.orientation_towards(target.rect.center))
            if self.rect_of_attack.colliderect(target.rect):
                if self.attack():
                    target.harm(self.firepower, "gunfire")
                    return [target]

    def name_and_rank(self):
        return "{0} {1}".format(self.ranks[self.rank], self.name)

    def promote(self):
        """ become a hardened veteran """
        if self.rank < len(Soldier.ranks) - 1:
            self.rank += 1
        # literally
        self.durability = self.durability + 1
