"""
  Facilities are laid out in an orderly grid as is the practice in
  all right-thinking and civilised nations.
"""
from pygame.rect import Rect
import unittest

SCREEN_HEIGHT = 768
SCREEN_WIDTH = 1024
LOT_WIDTH = 50
LOT_DEPTH = 40
NORTHERN_LIMIT = 168
SOUTHERN_LIMIT = SCREEN_HEIGHT - 120
EASTERN_LIMIT = SCREEN_WIDTH - 74
WESTERN_LIMIT = 0
FENCE_MARGIN_WEST = 5
FENCE_MARGIN_NORTH = 4

BOUNDS = Rect(WESTERN_LIMIT, NORTHERN_LIMIT,
              EASTERN_LIMIT - WESTERN_LIMIT,
              SOUTHERN_LIMIT - NORTHERN_LIMIT)

LOTS_NORTH = BOUNDS.height // LOT_DEPTH
LOTS_WEST = BOUNDS.width // LOT_WIDTH

WATER_RECT = Rect(905,382,40,152)

EDGE_TOLERANCE = 8

class TownPlanningOffice(object):
    """ Evaluate the proposed positions of facilities and
    equipment, determining an orderly position as close to
    the required on as is practicable. """

    def nearest_lot(self, x, y):
        """ The nearest entire lot on which a facility might be sited """
        if not BOUNDS.collidepoint(x,y):
            return None
        cx = (x - WESTERN_LIMIT) // LOT_WIDTH
        cy = (y - NORTHERN_LIMIT) // LOT_DEPTH
        lot = Rect(cx * LOT_WIDTH + WESTERN_LIMIT,
                    cy * LOT_DEPTH + NORTHERN_LIMIT,
                    LOT_WIDTH, LOT_DEPTH)
        if not WATER_RECT.colliderect(lot):
            return lot

    def nearest_edge(self, x, y):
        """ The nearest lot boundary on which a fence might be erected """
        lot = self.nearest_lot(x, y)
        if not lot:
            return None
        proximities = [(y - lot.top,"north"),
                       (lot.bottom-y,"south"),
                       (lot.right-x,"east"),
                       (x-lot.left,"west")]
        proximities.sort()
        closest = proximities[0]
        dist,side = closest
        if dist > EDGE_TOLERANCE:
            return None
        horizontal = (side=="north" or side=="south")
        vertical = (side=="east" or side=="west")
        if horizontal:
            rect = Rect(lot.left, lot.top - FENCE_MARGIN_NORTH, lot.width, 2*FENCE_MARGIN_NORTH)
            if side == "south":
                rect.move_ip(0, LOT_DEPTH)
            if not WATER_RECT.colliderect(rect):
                return rect
        elif vertical:
            rect = Rect(lot.left - FENCE_MARGIN_WEST, lot.top, 2*FENCE_MARGIN_WEST, lot.height)
            if side == "east":
                rect.move_ip(LOT_WIDTH, 0)
            if not WATER_RECT.colliderect(rect):
                return rect

def obstruance(*things):
    """ calculate the obstruance of a facility, unit or beast """
    bits = [{"all":63, "nothing":0, "fence":3, "hfence":1, "vfence":2,
             "unit":4, "beast":8, "facility":16, "land":32,
             "notland":31}.get(thing, 0)
            for thing in things]
    obst = 0
    for b in bits:
        obst |= b
    return obst


class DeterminationOfPlausibility(unittest.TestCase):
    def setUp(self):
        self.tpo = TownPlanningOffice()

    def test_too_far_north(self):
        self.assertEqual(self.tpo.nearest_lot(200, NORTHERN_LIMIT - 1), None)

    def test_too_far_south(self):
        self.assertEqual(self.tpo.nearest_lot(200, SOUTHERN_LIMIT + 1), None)

    def test_too_far_east(self):
        self.assertEqual(self.tpo.nearest_lot(EASTERN_LIMIT + 1, 300), None)

    def test_top_left(self):
        lot = self.tpo.nearest_lot(WESTERN_LIMIT + 1, NORTHERN_LIMIT + 1)
        self.assertTrue(lot)
        self.assertEqual(lot.width, LOT_WIDTH)
        self.assertEqual(lot.height, LOT_DEPTH)
        self.assertEqual(lot.left, WESTERN_LIMIT)
        self.assertEqual(lot.top, NORTHERN_LIMIT)

    def test_bot_right(self):
        lot = self.tpo.nearest_lot(EASTERN_LIMIT - 1, SOUTHERN_LIMIT - 1)
        self.assertTrue(lot)
        self.assertEqual(lot.width, LOT_WIDTH)
        self.assertEqual(lot.height, LOT_DEPTH)
        self.assertEqual(lot.right, EASTERN_LIMIT)
        self.assertEqual(lot.top, NORTHERN_LIMIT + (LOTS_NORTH - 1) * LOT_DEPTH)
        self.assertEqual(lot.bottom, SOUTHERN_LIMIT)

    def test_nofence_middle(self):
        lot = self.tpo.nearest_lot(417,317)
        self.assertTrue(lot)
        x,y = lot.center
        self.assertEqual(self.tpo.nearest_edge(x, y), None)

    def test_fence_west(self):
        lot = self.tpo.nearest_lot(417,317)
        self.assertTrue(lot)
        x,y = lot.midleft
        r = self.tpo.nearest_edge(x,y)
        self.assertTrue(r)
        self.assertEqual(r.left, x - FENCE_MARGIN_WEST)
        self.assertEqual(r.width, 2*FENCE_MARGIN_WEST)
        self.assertEqual(r.height, LOT_DEPTH)

    def test_fence_east(self):
        lot = self.tpo.nearest_lot(417,317)
        self.assertTrue(lot)
        x,y = lot.midright
        r = self.tpo.nearest_edge(x,y)
        self.assertTrue(r)
        self.assertEqual(r.left, x - FENCE_MARGIN_WEST)
        self.assertEqual(r.width, 2*FENCE_MARGIN_WEST)
        self.assertEqual(r.height, LOT_DEPTH)

    def test_fence_north(self):
        lot = self.tpo.nearest_lot(417,317)
        self.assertTrue(lot)
        x,y = lot.midtop
        r = self.tpo.nearest_edge(x,y)
        self.assertTrue(r)
        self.assertEqual(r.top, y - FENCE_MARGIN_NORTH)
        self.assertEqual(r.height, 2*FENCE_MARGIN_NORTH)
        self.assertEqual(r.width, LOT_WIDTH)

    def test_fence_north(self):
        lot = self.tpo.nearest_lot(417,317)
        self.assertTrue(lot)
        x,y = lot.midbottom
        r = self.tpo.nearest_edge(x,y)
        self.assertTrue(r)
        self.assertEqual(r.top, y - FENCE_MARGIN_NORTH)
        self.assertEqual(r.height, 2*FENCE_MARGIN_NORTH)
        self.assertEqual(r.width, LOT_WIDTH)

    def test_no_fence_corner(self):
        lot = self.tpo.nearest_lot(417,317)
        self.assertTrue(lot)
        x,y = lot.topleft
        r = self.tpo.nearest_edge(x,y)
        self.assertEqual(r, None)

if __name__ == '__main__':
    unittest.main()
