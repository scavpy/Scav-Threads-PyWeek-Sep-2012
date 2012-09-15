"""
The Bestiary of Animals New to The Arts and Sciences
"""
from pygame.rect import Rect
import random
import units
import facilities
import grid
import phonographs

class Animal(units.Unit):
    """A description of the Animal"""
    notable_attributes = ("Durability","Voracity","Monstrosity",
                          "Infernality",
                          "Velocity","Destructiveness")
    name = "Some kind of animal"
    durability = 1
    voracity = 1
    velocity = 1
    monstrosity = 1
    destructiveness = 1
    infernality = 1
    rapidity = 1 # for animals, rapidity should maybe equal velocity
    depiction = "Animal.png"
    obstruance = grid.obstruance("beast")
    exclusion = grid.obstruance("notland")
    exploding_chromograph_name = "units/explosion.png"
    exploding_phonograph_name = "explosion.ogg"
    explosion_frames = 5
    aliment = None

    def __init__(self, location):
        super(Animal, self).__init__(location)
        self.orient(2)
        self.bored = False
        self.angry = False
        self.satiety = 0
        self.walking = True
        self.exploding = False
        self.blast_radius = self.footprint[0] * self.infernality

    def __repr__(self):
        return "{0}({1},damage={2})".format(self.__class__.__name__,
                                        self.rect, self.damage)
    
    def attend_to_attack_area(self, centre):
        """ Beasts have close-in attacks """
        self.rect_of_attack.center = centre

    def going_the_wrong_way(self):
        right_ways = (5, 6, 7) if self.bored else (1, 2, 3)
        return self.orientation not in right_ways

    def go_the_right_way(self):
        right_ways = (5, 6, 7) if self.bored else (1, 2, 3)
        self.orient(random.choice(right_ways))

    def navigate(self, next_position):
        bounds = grid.BOUNDS
        if self.bored:
            self.maybe_explode()
        if grid.rect_in_bounds(next_position):
            self.move(next_position)
            # don't go the wrong way for long
            if self.going_the_wrong_way() and random.random() < 0.1:
                self.go_the_right_way()
            return
        if (next_position.right >= bounds.right or
            grid.in_water(next_position)):
            self.bored = True
            self.orient(6) # go straight back
            return
        if next_position.left <= 0:
            self.move(next_position)
            if self.bored:
                if next_position.right < 0:
                    self.finished = True
            else:
                self.go_the_right_way()
            return
        if next_position.top < bounds.top:
            self.orient(5 if self.bored else 3)
            return
        if next_position.bottom >= bounds.bottom:
            self.orient(7 if self.bored else 1)
            return

    def deal_with_obstacles(self, obstacles):
        """ attack whatever is in the way """
        indices = self.rect_of_attack.collidelistall(obstacles)
        if indices:
            categories = grid.obstruance("unit","facility","fence")
            targets = [obstacles[i] for i in indices 
                       if obstacles[i].obstruance & categories
                       and not obstacles[i].destroyed()]
            if targets and not self.attacking:
                target = targets[0]
                if self.attack():
                    target.harm(self.destructiveness, "trampled")
                    self.maybe_explode()
                    return [target]
        directions = (0,1,2,3,4,5,6,7) + ((4,5,6) if self.bored else (1,2,3))
        self.orient(random.choice(directions))

    def seek_food(self, knowledge, kind="Vegetable"):
        """ seek food of the preferred kind """
        targets = self.find_nearest(f for f in knowledge
                                    if f.aliment == kind
                                    and not f.destroyed())
        if targets:
            target = targets[0]
            self.orient(self.orientation_towards(target.rect.center))
            if not self.attacking:
                if self.rect_of_attack.colliderect(target.rect):
                    self.attack()
                    target.harm(1,"eaten")
                    self.satiety += 1
                    if self.satiety >= self.voracity:
                        self.bored = True
                    return [target]

    def explode(self):
        """ The purpose of this operation requires little explanation.
        Unlike the phenomemon itself, which makes no sense at all.
        """
        self.exploding = True
        self.obstruance = 0
        self.pace = 40
        self.animated_chromograph_name = self.exploding_chromograph_name
        self.attacking_animations = self.explosion_frames
        self.walking_animations = 0
        self.animation_frame = 1
        self.attacking = True
        self.rect_of_awareness.center = self.rect.center
        self.orientation_indices = (0,) * 8
        self.image = self.obtain_frame()
        phonographs.play(self.exploding_phonograph_name)

    def maybe_explode(self):
        if random.random()*100 < self.infernality:
            self.explode()

    def damage_surrounding_area(self, things):
        if not self.attacking:
            #explosion is over
            self.finished = True
            return
        indices = self.rect_of_awareness.collidelistall(things)
        quadrate_radius = self.blast_radius ** 2
        targets = []
        
        def quadrate_distance(other):
            ox, oy = other.rect.center
            sx, sy = self.rect.center
            dx2 = (ox - sx)**2
            dy2 = (oy - sy)**2
            return dx2 + dy2
        
        for i in indices:
            thing = things[i]
            if thing.destroyed():
                continue
            d = quadrate_distance(thing)
            if d > quadrate_radius:
                continue
            thing.harm(self.infernality, "exploded")
            targets.append(thing)
        return targets

    def harm(self, quanta_of_destruction, cause):
        """ Dinosaurs will sometimes explode for no readily apparent reason """
        super(Animal, self).harm(quanta_of_destruction, cause)
        if not self.destroyed:
            self.maybe_explode()

class Trinitroceratops(Animal):
    """What do these beasts want? To rut and feed and trample with
    abandon. Mere fences are little use against their horns.
    However they are slow to anger and easily pacified with food."""
    name = "Trinitroceratops horridus"
    durability = 50
    voracity = 18
    velocity = 5
    rapidity = 5
    monstrosity = 1
    destructiveness = 5
    infernality = 8
    depiction = "Trinitroceratops.png"
    animated_chromograph_name = "units/trinitroceratops.png"
    walking_animations = 2
    attacking_animations = 1
    orientation_indices = (1,0,0,0,0,1,1,1)
    footprint = (45,20)
    area_of_awareness = (100,80)
    area_of_attack = (25,20)
    attack_phonograph = "munching.ogg"

    def __init__(self, location):
        super(Trinitroceratops, self).__init__(location)

    def think(self, things):
        """ Determine the volition of the beast.
        If it act upon any thing else, return a list of such
        things. Otherwise return a non-true value.
        """
        if self.exploding:
            return self.damage_surrounding_area(things)        
        knowledge = self.things_perceived(things)
        next_position = self.step_position()
        obstacles = self.find_obstacles(next_position, knowledge)
        if obstacles:
            return self.deal_with_obstacles(obstacles)
        if not self.bored:
            food = self.seek_food(knowledge, "Vegetable")
            if food:
                return food
        self.navigate(next_position)

class Explodocus(Animal):
    """Science is dumbfounded and reason fails in explaining this monster.
    It is advisable to either slay the beast quickly and far from your
    facilities, or else leave it be entirely. """
    name = "Explodocus catastrophii"
    durability = 200
    voracity = 30
    velocity = 3
    rapidity = 3
    monstrosity = 4
    infernality = 10
    depiction = "Explodocus.png"
    animated_chromograph_name = "units/explodocus.png"
    exploding_chromograph_name = "units/superexplode.png"
    explosion_frames = 5
    walking_animations = 3
    attacking_animations = 0
    orientation_indices = (1,0,0,0,0,1,1,1)
    footprint = (70,56)
    area_of_awareness = (200, 160)
    area_of_attack = (75,61)
    attack_phonograph = "munching.ogg"

    def __init__(self, location):
        super(Explodocus, self).__init__(location)

    def think(self, things):
        """ Determine the volition of the beast.
        If it act upon any thing else, return a list of such
        things. Otherwise return a non-true value.
        """
        if self.exploding:
            return self.damage_surrounding_area(things)        
        knowledge = self.things_perceived(things)
        next_position = self.step_position()
        obstacles = self.find_obstacles(next_position, knowledge)
        if obstacles:
            return self.deal_with_obstacles(obstacles)
        if not self.bored:
            food = self.seek_food(knowledge, "Vegetable")
            if food:
                return food
        self.navigate(next_position)

    def attend_to_attack_area(self, ignored):
        """ Explodocus tramples all round at close range """
        self.rect_of_attack.center = self.rect.center

        

class Tankylosaurus(Animal):
    """A thoroughly bad-tempered beast and very sturdy but at least its
    appetite is modest"""
    name = "Tankylosaurus iracundus"
    durability = 150
    voracity = 6
    velocity = 4
    rapidity = 5
    monstrosity = 2
    destructiveness = 4
    depiction = "Tankylosaurus.png"
    animated_chromograph_name = "units/tankylosaurus.png"
    walking_animations = 2
    attacking_animations = 2
    orientation_indices = (1,0,0,0,0,1,1,1)
    footprint = (40,32)
    area_of_awareness = (100,80)
    area_of_attack = (45,40) # special
    attack_phonograph = "growl.ogg"

    def __init__(self, location):
        super(Tankylosaurus, self).__init__(location)
        self.angry = True

    def attend_to_attack_area(self, ignored):
        """ Tankylosaurus can attack all round at close range """
        self.rect_of_attack.center = self.rect.center

    def think(self, things):
        """ Determine the volition of the beast.
        If it act upon any thing else, return a list of such
        things. Otherwise return a non-true value.
        """
        if self.exploding:
            return self.damage_surrounding_area(things)
        knowledge = self.things_perceived(things)
        next_position = self.step_position()
        obstacles = self.find_obstacles(next_position, knowledge)
        if obstacles:
            return self.deal_with_obstacles(obstacles)
        if not self.attacking:
            targets = self.random_malice(knowledge)
            if targets:
                return targets
        if not self.bored:
            food = self.seek_food(knowledge, "Vegetable")
            if food:
                return food
        self.navigate(next_position)

    def random_malice(self, things):
        """ Vent spleen on all things within reach """
        indices = self.rect_of_attack.collidelistall(things)
        targets = [things[i] for i in indices
                   if things[i].obstruance & grid.obstruance("fence", "facility", "unit")
                   and not things[i].destroyed()]
        if targets:
            self.attack()
        for target in targets:
            target.harm(self.destructiveness, "trampled")
        return targets

class Ferociraptor(Animal):
    """ A deadly and swift predator. Our foremost zoologist only
    managed to shoot one of them for study before he was ambushed
    and eaten by two others."""
    name = "Ferociraptor incandescens"
    durability = 11
    voracity = 12
    velocity = 8
    infernality = 2
    monstrosity = 5
    destructiveness = 2
    depiction = "Ferociraptor.png"
    animated_chromograph_name = "units/ferociraptor.png"
    walking_animations = 2
    attacking_animations = 2
    orientation_indices = (1,0,0,0,0,1,1,1)
    footprint = (15,12)
    area_of_awareness = (150,120)
    area_of_attack = (10,8)
    attack_phonograph = "raptor.ogg"

    def __init__(self, location):
        super(Ferociraptor, self).__init__(location)


    def think(self, things):
        """ Determine the volition of the beast.
        If it act upon any thing else, return a list of such
        things. Otherwise return a non-true value.
        """
        if self.exploding:
            return self.damage_surrounding_area(things)        
        knowledge = self.things_perceived(things)
        next_position = self.step_position()
        obstacles = self.find_obstacles(next_position, knowledge)
        if obstacles:
            if random.random() < 0.5:
                return self.deal_with_obstacles(obstacles)
            else:
                self.orient(random.randint(0,7))
        if not self.bored:
            food = self.seek_food(knowledge, "Meat")
            if food:
                return food
        self.navigate(next_position)


class Blastosaurus(Animal):
    """ King of the exploding dinosaurs. The most monstrous and
    voratious eater of men, and a dangerously explosive creature
    best dispatched well away from any important structures."""
    name = "Blastosaurus rex"
    durability = 70
    voracity = 18
    velocity = 5
    infernality = 3
    monstrosity = 8
    destructiveness = 7
    depiction = "Blastosaurus.png"
    animated_chromograph_name = "units/blastosaurus.png"
    walking_animations = 2
    attacking_animations = 1
    orientation_indices = (1,0,0,0,0,1,1,1)
    footprint = (45,33)
    area_of_awareness = (150,120)
    area_of_attack = (20,16)
    attack_phonograph = "b-rex-mono.ogg"

    def __init__(self, location):
        super(Blastosaurus, self).__init__(location)


    def think(self, things):
        """ Determine the volition of the beast.
        If it act upon any thing else, return a list of such
        things. Otherwise return a non-true value.
        """
        if self.exploding:
            return self.damage_surrounding_area(things)        
        knowledge = self.things_perceived(things)
        next_position = self.step_position()
        obstacles = self.find_obstacles(next_position, knowledge)
        if obstacles:
            if random.random() < 0.8:
                return self.deal_with_obstacles(obstacles)
            else:
                self.orient(random.randint(0,7))
        if not self.bored:
            food = self.seek_food(knowledge, "Meat")
            if food:
                return food
        self.navigate(next_position)
