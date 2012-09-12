"""
The Bestiary of Animals New to The Arts and Sciences
"""
from pygame.rect import Rect
import random
import units
import facilities
import grid

class Animal(units.Unit):
    """A description of the Animal"""
    notable_attributes = ("Durability","Voracity","Monstrosity",
                          "Velocity","Destructiveness")
    name = "Some kind of animal"
    durability = 1
    voracity = 1
    velocity = 1
    monstrosity = 1
    destructiveness = 1
    rapidity = 1 # for animals, rapidity should maybe equal velocity
    depiction = "Animal.png"
    obstruance = grid.obstruance("beast")
    exclusion = grid.obstruance("notland")
    aliment = None

    def attend_to_attack_area(self, centre):
        """ Beasts have close-in attacks """
        self.rect_of_attack.center = centre


class Trinitroceratops(Animal):
    """What do these beasts want? To rut and feed and trample with
    abandon. Mere fences are little use against their horns.
    However they are slow to anger and easily pacified with food."""
    name = "Trinitroceratops horridus"
    durability = 30
    voracity = 4
    velocity = 5
    rapidity = 5
    monstrosity = 1
    destructiveness = 5
    depiction = "Trinitroceratops.png"
    animated_chromograph_name = "units/trinitroceratops.png"
    walking_animations = 2
    attacking_animations = 1
    orientation_indices = (1,0,0,0,0,1,1,1)
    footprint = (45,20)
    area_of_awareness = (100,80)
    area_of_attack = (30,24)

    def __init__(self, location):
        super(Trinitroceratops, self).__init__(location)
        self.orient(2)
        self.bored = False
        self.angry = False
        self.satiety = 0
        self.walking = True

    def think(self, things):
        """ Determine the volition of the beast.
        If it act upon any thing else, return a list of such
        things. Otherwise return a non-true value.
        """
        knowledge = self.things_perceived(things)
        next_position = self.step_position()
        obstacles = self.find_obstacles(next_position, knowledge)
        if obstacles:
            indices = self.rect_of_attack.collidelistall(obstacles)
            if indices:
                categories = grid.obstruance("unit","facility","fence")
                targets = [obstacles[i] for i in indices 
                           if obstacles[i].obstruance & categories]
                if targets and not self.attacking:
                    target = targets[0]
                    self.attack()
                    target.harm(self.destructiveness)
                    return [target]
            directions = (0,1,2,3,4,5,6,7) + ((4,5,6) if self.bored else (1,2,3))
            self.orient(random.choice(directions))
            return
        elif not self.bored:
            targets = self.find_nearest(f for f in knowledge
                                        if f.aliment == "Vegetable"
                                        and not f.destroyed())
            if targets:
                target = targets[0]
                self.orient(self.orientation_towards(target.rect.center))
                if not self.attacking:
                    if self.rect_of_attack.colliderect(target.rect):
                        self.attack()
                        target.harm(1)
                        self.satiety += 1
                        if self.satiety >= self.voracity:
                            self.bored = True
                        return [target]
        self.navigate(next_position)

    def step_position(self):
        """ where will it be on the next step? """
        if self.walking:
            vector = units.octoclock_direction(self.orientation, self.directions)
            next_position = self.rect.move(vector)
        else:
            next_position = self.rect
        return next_position


    def navigate(self, next_position):
        bounds = grid.BOUNDS
        if bounds.contains(next_position):
            self.move(next_position)
            return
        if next_position.right >= bounds.right:
            self.bored = True
            self.orient(6) # go back
            return
        if next_position.left <= 0:
            self.move(next_position)
            if self.bored:
                if next_position.right < 0:
                    self.finished = True
            else:
                self.orient(random.randint(1,3))
            return
        if next_position.top < bounds.top:
            self.orient(5 if self.bored else 3)
            return
        if next_position.bottom >= bounds.bottom:
            self.orient(7 if self.bored else 1)
            return


