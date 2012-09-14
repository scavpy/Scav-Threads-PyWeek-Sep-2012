"""
 Chapters of the adventure, with their prefatory announcements et cetera.
"""
from pygame import Rect
import bestiary
import facilities
import units

class Chapter(object):
    """ A container for information about a chapter """
    def __init__(self, number, subtitle="", illustration="",
                 summary="", waves=[], inventions=[]):
        self.number = number
        self.subtitle = subtitle
        self.illustration = illustration
        self.summary = summary
        self.waves = waves
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
            wave_of("Ferociraptor", -50, 200, 240, 500, 550),
            wave_of("Ferociraptor", -50, 200, 240, 500, 550),
            wave_of("Ferociraptor", -50, 200, 240, 500, 550) + wave_of("Trinitroceratops", -80, 360, 450)
            ],
        inventions=[("units", "Cannon"), ("fences","Fence")]
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
        inventions=[("units","AnalyticalCannon"), ("fences","Wall")]
        ),
    Chapter(
        "Three","Desperate Times","boat.png",
        " Our defences are weakened and our resources badly stretched"
        " by these monstrous herbivores.\n"
        " God grant that nothing worse comes our way!",
        waves=[
            wave_of("Trinitroceratops", -50, 200, 240, 500, 550) + wave_of("Tankylosaurus", -150, 300, 400),
            wave_of("Trinitroceratops", -50, 200, 240, 500, 550) + wave_of("Tankylosaurus", -150, 300, 400),
            wave_of("Trinitroceratops", -50, 200, 550) + wave_of("Tankylosaurus", -150, 300, 400) + [("Blastosaurus", -80, 330)]
            ],
        inventions=[]
        ),
]
    
