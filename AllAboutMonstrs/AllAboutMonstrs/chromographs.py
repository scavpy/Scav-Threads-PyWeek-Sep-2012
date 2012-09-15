"""
 Much use is made of tesselated chromographs to depict the
 dramatis personae, exotic scenery and technological marvels
 of this tale.
"""
import os
import pygame
import data
from pygame.rect import Rect

CHROMOGRAPHS = {}
PORTIONS = {}
FRAMES = {}

def obtain(chromograph_name):
    chromograph = CHROMOGRAPHS.get(chromograph_name)
    if not chromograph:
        try:
            path = data.filepath(
                os.path.join("tessellated_chromographs", chromograph_name))
            chromograph = pygame.image.load(path)
            if chromograph.get_flags() & pygame.SRCALPHA:
                chromograph = chromograph.convert_alpha()
            else:
                chromograph = chromograph.convert()
            CHROMOGRAPHS[chromograph_name] = chromograph
        except pygame.error:
            chromograph = pygame.surface.Surface((20,20))
            pygame.draw.line(chromograph, (255,0,0), (0,0), (20,20))
            pygame.draw.line(chromograph, (255,0,0), (20,0), (0,20))
    return chromograph

def obtain_portion(chromograph_name, portion):
    key = "{0}{1}".format(chromograph_name, portion)
    chromograph = PORTIONS.get(key)
    if not chromograph:
        surface = obtain(chromograph_name)
        try:
            chromograph = surface.subsurface(portion)
        except ValueError:
            portion.topleft = (0,0)
            portion.height = min(surface.height,portion.height)
            portion.width = min(surface.width,portion.width)
            chromograph = surface.subsurface(portion)            
        PORTIONS[key] = chromograph
    return chromograph

def obtain_frame(chromograph_name, frame_col, frame_row, frames_wide, frames_tall):
    key = "{0}-{1}of{3},{2}of{4}".format(chromograph_name,
                                         frame_col,
                                         frame_row,
                                         frames_wide,
                                         frames_tall)
    chromograph = FRAMES.get(key)
    if not chromograph:
        surface = obtain(chromograph_name)
        frame_col = min(max(0,frame_col),frames_wide-1)
        frame_row = min(max(0,frame_row),frames_tall-1)
        width, height = surface.get_size()
        portion_width = width // frames_wide
        portion_height = height // frames_tall
        portion = Rect(portion_width * frame_col,
                       portion_height * frame_row,
                       portion_width,
                       portion_height)
        chromograph = obtain_portion(chromograph_name, portion)
        FRAMES[key] = chromograph
    return chromograph
