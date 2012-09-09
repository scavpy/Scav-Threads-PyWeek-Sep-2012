"""
  Facilities are laid out in an orderly grid as is the practice in
  all right-thinking and civilised nations.
"""
from __main__ import SCREENRES
from pygame.rect import Rect

LOT_WIDTH = 50
LOT_DEPTH = 40
NORTHERN_LIMIT = 168
SOUTHERN_LIMIT = 100
EASTERN_LIMIT = 124
WESTERN_LIMIT = 0
FENCE_MARGIN = 10

LOTS_NORTH = (SCREENRES[1] - (NORTHERN_LIMIT + SOUTHERN_LIMIT)) // LOT_DEPTH
LOTS_WEST = (SCREENRES[0] - (EASTERN_LIMIT + WESTERN_LIMIT)) // LOT_WIDTH

class TownPlanningOffice(object):
    """ Evaluate the proposed positions of facilities and
    equipment, determining an orderly position as close to
    the required on as is practicable. """

    def nearest_cell(self, x, y):
        """ The nearest entire lot on which a facility might be sited """
        cx = (x - WESTERN_LIMIT) // LOT_WIDTH
        cy = (y - NORTHERN_LIMIT) // LOT_DEPTH
        return Rect(cx * LOT_WIDTH + WESTERN_LIMIT,
                    cy * LOT_DEPTH + NORTHERN_LIMIT,
                    LOT_WIDTH, LOT_DEPTH)

    def nearest_edge(self, x, y):
        """ The nearest lot boundary on which a fence might be erected """
        
