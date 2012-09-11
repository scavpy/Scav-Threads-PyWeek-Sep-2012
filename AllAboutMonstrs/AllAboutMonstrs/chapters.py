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

CHAPTERS = [
    Chapter("One","A Reptilian Assault","boat.png",
            " Shortly after arriving upon the island, we met with \
the reptiles. Their incendiary properties are much worse than we \
could have predicted.\n Worse still, it would appear that they have \
developed an appetite for the tar on our ships. We have but five \
vessels remaining and must protect them at all costs.",
            waves = [
                [("Trinitroceratops", -20, 200),
                 ("Trinitroceratops", -30, 220),
                 ("Trinitroceratops", -20, 500),
                 ("Trinitroceratops", -30, 550)],
                [("Trinitroceratops", -20, 200),
                 ("Trinitroceratops", -30, 220),
                 ("Trinitroceratops", -20, 500),
                 ("Trinitroceratops", -30, 550)],
                [("Trinitroceratops", -20, 220),
                 ("Trinitroceratops", -30, 230),
                 ("Trinitroceratops", -80, 500),
                 ("Trinitroceratops", -70, 200),
                 ("Trinitroceratops", -20, 500),
                 ("Trinitroceratops", -30, 550)],
                ],
            inventions = [("units", "Cannon")]),
    ]
    
