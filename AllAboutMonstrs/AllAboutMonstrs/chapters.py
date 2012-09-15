"""
 Chapters of the adventure, with their prefatory announcements et cetera.
"""
from pygame import Rect
import bestiary
import random
import grid

class Chapter(object):
    """ A container for information about a chapter """
    def __init__(self, number, subtitle="", illustration="",
                 summary="", waves=(), fences=(),
                 facilities=(), inventions=()):
        self.number = number
        self.subtitle = subtitle
        self.illustration = illustration
        self.summary = summary
        self.waves = waves
        self.fences = fences
        self.facilities = facilities
        self.inventions = inventions

    def spawn_wave(self, number):
        """ a collection of beasts """
        beasts = []
        if 0 <= number < len(self.waves):
            wave = self.waves[number]
            for genus, west, south in wave:
                location = Rect(0,0,1,1)
                location.center = (west, south)
                beasts.append(getattr(bestiary, genus)(location))
        return beasts

    def beasts_in_this_chapter(self):
        seen = []
        for wave in self.waves:
            for genus, west, south in wave:
                if genus not in seen:
                    seen.append(genus)
        return seen

def wave_of(genus, column, *rows):
    return [(genus, column, row) for row in rows]

CHAPTERS = [
    Chapter(
        "One","A Reptilian Assault","boat.png",
        " Shortly after arriving upon the island, we met with \
the reptiles. Their incendiary properties are much worse than we \
could have predicted.\n Worse still, it would appear that they have \
developed an appetite for the coal on our ships. We have but four \
vessels remaining and must protect them at all costs.",
        waves=[
            wave_of("Ferociraptor", -50, 200, 240, 300, 500, 550),
            wave_of("Ferociraptor", -50, 200, 240, 300, 500, 550) + [("Trinitroceratops", -100, 400)],
            wave_of("Ferociraptor", -50, 200, 240, 500, 550) + wave_of("Trinitroceratops", -100, 300, 360, 410)
            ],
        inventions=["Cannon"], fences=["Fence"],
        ),
    Chapter(
        "Two","Desperate Times","boat.png",
        " The intensity of the assaults by the saurian "
        " monstrosities never diminishes.\n Our scientists"
        " are ever working on new developments to help"
        " fight them off.",
        waves=[
            wave_of("Trinitroceratops", -50, 200, 240, 300, 430, 550) + wave_of("Ferociraptor", -150, 300, 400, 500),
            wave_of("Trinitroceratops", -50, 200, 240, 300, 430, 550) + wave_of("Ferociraptor", -150, 300, 400, 500),
            wave_of("Trinitroceratops", -50, 200, 240, 300, 430, 550) + wave_of("Tankylosaurus", -150, 300, 400)
            ],
        inventions=["AnalyticalCannon"], fences=["Wall"],
        ),
    Chapter(
        "Three","Calm Before The Storm","boat.png",
        " Our defences are weakened and our resources badly stretched"
        " by these monstrous herbivores.\n"
        " God grant that nothing worse comes our way!",
        waves=[
            wave_of("Trinitroceratops", -50, 200, 240, 500, 550) + wave_of("Tankylosaurus", -150, 300, 400),
            wave_of("Trinitroceratops", -50, 200, 240, 500, 550) + wave_of("Tankylosaurus", -150, 300, 400),
            wave_of("Trinitroceratops", -50, 200, 550) + wave_of("Tankylosaurus", -150, 300, 400) + [("Blastosaurus", -80, 330)]
            ],
        ),
]

def last_chapter():
    return len(CHAPTERS) - 1

def random_wave(dino_names, hoard_size):
    wave = []
    for i in xrange(hoard_size):
        wave.append((random.choice(dino_names),
                     random.randint(-800, -20),
                     random.randint(grid.NORTHERN_LIMIT + 30, grid.SOUTHERN_LIMIT - 30)))
    return wave
    
def open_chapter(n):
    if n <= last_chapter():
        return CHAPTERS[n]
    fences = []
    tech = []
    if n == 3:
        fences.append("ConcreteWall")
    elif n == 4:
        tech.append("SteamCavalry")
    chapter = Chapter(str(n + 1), "Yet Worse Onslaughts", "bonus.png",
                      " After you returned, notionally victorious,"
                      " the colony continued to suffer increasingly"
                      " serious attacks.", waves=[], fences=fences, inventions=tech)
    assert chapter.illustration
    kinds = ["Ferociraptor"]
    if n & 1:
        kinds.append("Trinitroceratops")
    if n & 2:
        kinds.append("Tankylosaurus")
    if n & 4:
        kinds.append("Blastosaurus")
    if n & 8:
        kinds.append("Explodocus")
    dinos_per_wave = 6 + 3 * n
    for wave in 0,1,2:
        chapter.waves.append(random_wave(kinds, dinos_per_wave + wave))
    return chapter
    
