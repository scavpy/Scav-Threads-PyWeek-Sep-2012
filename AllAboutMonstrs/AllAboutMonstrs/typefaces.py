"""
Here the movable typefaces are cast in readiness for use in
publications intended for the edification and instruction of
the operator.
"""

import pygame.font
from pygame.font import Font
from pygame.surface import Surface
import data

STYLE_SIZES = {
    "title":48,
    "subtitle":32,
    "normal":24,
    "small":16,
    }

FONTS = {}

def init():
    pygame.font.init()
    path = data.filepath("Anaktoria.otf")
    for appelation, size in STYLE_SIZES.items():
        FONTS[appelation] = Font(path, size)

init()

def prepare(text, size="normal", colour=(0,0,0)):
    """ prepare a section of text """
    f = FONTS[size]
    return f.render(text, True, colour)

def prepare_title(text, colour=(0,0,0)):
    """ prepare text as a title """
    return prepare(text, size="title", colour=colour)

def prepare_subtitle(text, colour=(0,0,0)):
    """ prepare text as a subtitle """
    return prepare(text, size="subtitle", colour=colour)

def prepare_table(rows, alignment="lr", size="normal", colour=(0,0,0), padding=0):
    f = FONTS[size]
    numcolumns = len(rows[0])
    numrows = len(rows)
    def u(n):
        return n if isinstance(n, unicode) else unicode(n)
    shapes = [[f.size(u(col)) for col in row] for row in rows]
    maxheight = max(max(shape[1] for shape in shaperow) for shaperow in shapes)
    widths = [max(shaperow[i][0] for shaperow in shapes) for i in range(numcolumns)]
    table = Surface((sum(widths) + padding * (numcolumns - 1),
                     maxheight * numrows + padding * (numrows - 1)),
                    pygame.SRCALPHA)
    table.fill((255,255,255,0))
    y = 0
    for r, row in enumerate(rows):
        x = 0
        for c, col in enumerate(row):
            w, h = shapes[r][c]
            text = prepare(u(col), size=size, colour=colour)
            align = alignment[c]
            if align == "r":
                adjustx = widths[c] - w
            elif align == "c":
                adjustx = (widths[c] - w) // 2
            else:
                adjustx = 0
            table.blit(text, (x + adjustx, y))
            x += widths[c] + padding
        y += maxheight + padding
    return table

def prepare_paragraph(text, width, size="normal", colour=(0,0,0)):
    font = FONTS[size]
    lines = []
    words = text.split()
    lastline = None
    line = words[0]
    for i in range(1,len(words)):
        lastline = line
        line = line+" "+words[i]
        w,h = font.size(line)
        if w > width:
            lines.append(lastline)
            line = words[i]
    lines.append(line)

    parawidth = max(font.size(each)[0] for each in lines)
    lineheight = font.get_height()
    paraheight = lineheight*len(lines)
    paragraph = Surface((parawidth,paraheight),pygame.SRCALPHA)
    paragraph.fill((255,255,255,0))
    for y,line in enumerate(lines):
        text = prepare(line,size,colour)
        paragraph.blit(text,(0,y*lineheight))
    return paragraph

def prepare_passage(text, width, size="normal", colour=(0,0,0)):
    sections = text.split("\n")
    paras = [prepare_paragraph(t,width,size=size,colour=colour)
             for t in sections]
    fullwidth = max(p.get_width() for p in paras)
    fullheight = sum(p.get_height() for p in paras)
    passage = Surface((fullwidth,fullheight),pygame.SRCALPHA)
    passage.fill((255,255,255,0))
    y = 0
    for p in paras:
        passage.blit(p,(0,y))
        y += p.get_height()
    return passage
    
