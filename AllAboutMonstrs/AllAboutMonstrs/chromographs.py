"""
 Much use is made of tesselated chromographs to depict the
 dramatis personae, exotic scenery and technological marvels
 of this tale.
"""
import os
import pygame
import data

CHROMOGRAPHS = {}

def obtain(chromograph_name):
    chromograph = CHROMOGRAPHS.get(chromograph_name)
    if not chromograph:
        try:
            path = data.filepath(
                os.path.join("tessellated_chromographs", chromograph_name))
            chromograph = pygame.image.load(path)
            CHROMOGRAPHS[chromograph_name] = chromograph
        except pygame.error:
            chromograph = pygame.surface.Surface((20,20))
            pygame.draw.line(chromograph, (255,0,0), (0,0), (20,20))
            pygame.draw.line(chromograph, (255,0,0), (20,0), (0,20))
    return chromograph

