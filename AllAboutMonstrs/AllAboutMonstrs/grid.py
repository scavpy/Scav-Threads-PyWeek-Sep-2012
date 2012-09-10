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
EASTERN_LIMIT = SCREEN_WIDTH - 124
WESTERN_LIMIT = 0
FENCE_MARGIN_WEST = 5
FENCE_MARGIN_NORTH = 4

LOTS_NORTH = (SOUTHERN_LIMIT - NORTHERN_LIMIT) // LOT_DEPTH
LOTS_WEST = (EASTERN_LIMIT - WESTERN_LIMIT) // LOT_WIDTH

class TownPlanningOffice(object):
    """ Evaluate the proposed positions of facilities and
    equipment, determining an orderly position as close to
    the required on as is practicable. """

    def nearest_lot(self, x, y):
        """ The nearest entire lot on which a facility might be sited """
        if (x < WESTERN_LIMIT
            or x >= EASTERN_LIMIT
            or y < NORTHERN_LIMIT
            or y >= SOUTHERN_LIMIT):
            return None
        cx = (x - WESTERN_LIMIT) // LOT_WIDTH
        cy = (y - NORTHERN_LIMIT) // LOT_DEPTH
        return Rect(cx * LOT_WIDTH + WESTERN_LIMIT,
                    cy * LOT_DEPTH + NORTHERN_LIMIT,
                    LOT_WIDTH, LOT_DEPTH)

    def nearest_edge(self, x, y):
        """ The nearest lot boundary on which a fence might be erected """
        lot = self.nearest_lot(x, y)
        if not lot:
            return None
        xprop = (x - lot.left) / float(LOT_WIDTH)
        yprop = (y - lot.top) / float(LOT_DEPTH)
        north_edge = yprop < 0.25
        south_edge = yprop > 0.75
        west_edge = xprop < 0.25
        east_edge = xprop > 0.75
        horizontal = (north_edge or south_edge) and not (east_edge or west_edge)
        vertical = (east_edge or west_edge) and not (north_edge or south_edge)
        if horizontal:
            rect = Rect(lot.left, lot.top - FENCE_MARGIN_NORTH, lot.width, 2*FENCE_MARGIN_NORTH)
            if south_edge:
                rect.movei(0, LOT_DEPTH)
            return rect
        elif vertical:
            rect = Rect(lot.left - FENCE_MARGIN_WEST, lot.top, 2*FENCE_MARGIN_WEST, lot.height)
            if east_edge:
                rect.movei(LOT_WIDTH, 0)
            return rect
        else:
            return None

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
