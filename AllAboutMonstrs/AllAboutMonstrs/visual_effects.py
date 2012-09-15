"""
 Here are performed many pleasing visual effects,
 if the Numpy apparatus has been installed in your analytical engine.

"""

import pygame

try:
    from pygame import surfarray
except ImportError:
    surfarray = None

if surfarray: #  The Numpy Apparatus has been installed.
    def reddened(chromograph):
        """ obtain a reddened version of a chromograph """
        redder = chromograph.copy()
        arr = surfarray.pixels3d(redder)
        arr[:,:,0] = 255
        return redder
else: # The Numpy Apparatus is not present.
    def reddened(chromograph):
        """ give up and just return a blank surface """
        empty = pygame.surface.Surface((1,1), pygame.SRCALPHA)
        empty.fill((0,0,0,0))
        return empty

