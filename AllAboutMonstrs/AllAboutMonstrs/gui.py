import pygame
from pygame.transform import flip,scale

import chromographs
import typefaces
import facilities
import units
from accounting_mode import lsb

from math import sin, cos, sqrt, radians

def make_textbox(position,text,width,size="normal",colour=(0,0,0)):
    widget = SurfWidget(
        typefaces.prepare_passage(text,width,size=size,colour=colour))
    return TextFrame(position,[widget],width)

def make_titledbox(position,title,text,width,titlesize="subtitle",
                   textsize="normal",gap=12,indent=20,colour=(0,0,0)):
    titlewidget = SurfWidget(
        typefaces.prepare(title,size=titlesize,colour=colour))
    textwidget = SurfWidget(
        typefaces.prepare_passage(text,width-indent*2,size=textsize,colour=colour))
    return TextFrame(position,
                     [titlewidget,
                      SpaceWidget(gap),
                      textwidget],width)

def make_menu(position,options,width,prompt=None):
    contents = []
    if prompt:
        p = SurfWidget(typefaces.prepare_paragraph(prompt,width))
        contents.append(p)
        contents.append(SpaceWidget(8))
    for label,command in options:
        o = ChoiceWidget(label,command)
        contents.append(o)
    return TextFrame(position,contents,width)

class BuildMenu(object):
    gear = chromographs.obtain("iconic/gear.png")
    gearrect = gear.get_rect()
    optrad = 32

    def __init__(self, situation):
        self.is_open = False
        self.facs = []
        self.units = []
        self.options = []
        self.position = (0,0)
        self.centerrect = pygame.Rect(0,0,64,64)
        self.situation = situation

    def open_menu(self,position,edge=False):
        self.is_open = True
        self.position = position
        self.centerrect.center = self.position
        if edge:
            self.facs = self.situation.fence_plans
        else:
            self.facs = self.situation.facility_plans
        self.units = self.situation.unit_plans
        self.options = self.halfwheel(facilities,self.facs,-1)
        self.options.extend(self.halfwheel(units,self.units,1))
        self.options.append((None,None,self.centerrect))

    def close_menu(self):
        self.is_open = False

    def halfwheel(self,module,items,hemisphere):
        x,y = self.position
        result = []
        r = self.optrad*2
        angle = hemisphere * radians(180.0/(len(items)+1))
        for i,item in enumerate(items):
            itemclass = getattr(module,item,None)
            img = chromographs.obtain("iconic/%s.png"%item)
            rect = img.get_rect()
            rect.center = (x + cos(angle*(i+1))*r, y + sin(angle*(i+1))*r)
            opt = (itemclass,img,rect)
            result.append(opt)
        return result

    def render(self,screen):
        g = self.gear
        gr = self.gearrect
        for itemclass,image,rect in self.options:
            gr.center = rect.center
            screen.blit(g,gr)
            if image:
                screen.blit(image,rect)

    def mouse_event(self, e):
        px,py = e.pos
        for itemclass,image,rect in self.options:
            if itemclass and self.situation.can_afford_a(itemclass):
                x,y = rect.center
                dx,dy = (px-x,py-y)
                dist2 = dx*dx+dy*dy
                if dist2 <= self.optrad*self.optrad:
                    return itemclass
        return None

class StatusBar(object):
    height = 120
    live_ship = chromographs.obtain("iconic/living-ship.png")
    dead_ship = chromographs.obtain("iconic/dead-ship.png")

    def __init__(self):
        self.stats_table = None
        self.remaining_ships = 0
        self.max_ships = 0

    def update(self, money, food, ships, remaining):
        self.stats_table = typefaces.prepare_table(
            [["Wealth",":  ",lsb(money)],
             ["Food",":  ",str(food)]],
            colour = (255,255,255), alignment="llr")
        self.remaining_ships = remaining
        self.max_ships = ships

    def render(self,screen):
        y = screen.get_height() - self.height
        pygame.draw.rect(screen,(0,0,0),(0,y,screen.get_width(),self.height))
        screen.blit(self.stats_table,(20,y+20))
        for i in range(self.max_ships):
            if i < self.remaining_ships:
                screen.blit(self.live_ship,(350+i*100,y+10))
            else:
                screen.blit(self.dead_ship,(350+i*100,y+10))

class TextFrame(object):
    head_end = chromographs.obtain("flourish/top-end.png")
    head_mid = chromographs.obtain("flourish/top-mid.png")
    head_line = chromographs.obtain("flourish/top-line.png")
    foot_end = chromographs.obtain("flourish/bottom-end.png")
    foot_line = chromographs.obtain("flourish/bottom-line.png")
    sel_mark = chromographs.obtain("flourish/select-marker.png")
    
    def __init__(self,position,contents,width,
                 fontsize="normal",colour=(0,0,0)):
        self.position = position
        self.contents = contents
        self.prepare_size(width)
        self.selected = None
        for i,c in enumerate(self.contents):
            c.set_master(self)
            if not self.selected and c.selectable:
                self.selected = (i,c)

    def content_size(self):
        width = max(c.width for c in self.contents)
        height = sum(c.height for c in self.contents)
        return (width,height)

    def prepare_size(self,asked_width):
        he = self.head_end
        hl = self.head_line
        hm = self.head_mid
        fe = self.foot_end
        fl = self.foot_line
        self.min_header_width = mhw = he.get_width()*2 + hm.get_width()
        self.min_footer_width = mfw = fe.get_width()*2
        cwidth,cheight = self.content_size()
        self.width = max(asked_width,cwidth,mhw,mfw)
        topgap = (self.width-self.min_header_width)/2
        bottomgap = self.width-self.min_footer_width
        self.top_line = scale(hl,(topgap,hl.get_height()))
        self.bottom_line = scale(fl,(bottomgap,fl.get_height()))
        self.headheight = he.get_height()
        self.footheight = fe.get_height()

    def render(self,screen):
        x,y = self.position
        cwidth,cheight = self.content_size()
        self.render_header(screen)
        mark = self.sel_mark
        dy = y+self.headheight
        for c in self.contents:
            surf = c.get_surface()
            if surf:
                indent = (self.width-c.width)/2
                if self.selected and c == self.selected[1]:
                    hh = (c.height-mark.get_height())/2
                    screen.blit(mark,(x+indent-mark.get_width(), dy+hh))
                    screen.blit(flip(mark,True,False),(x+indent+c.width, dy+hh))
                screen.blit(surf,(x+indent, dy))
            dy += c.height
        self.render_footer(screen)

    def render_header(self,screen):
        ew = self.head_end.get_width()
        lw = self.top_line.get_width()
        mw = self.head_mid.get_width()
        x,y = self.position
        screen.blit(self.head_end,(x,y))
        screen.blit(self.top_line,(x+ew,y))
        screen.blit(self.head_mid,(x+ew+lw,y))
        screen.blit(self.top_line,(x+ew+lw+mw,y))
        screen.blit(flip(self.head_end,True,False),(x+ew+2*lw+mw,y))

    def render_footer(self,screen):
        x,y = self.position
        cwidth,cheight = self.content_size()
        y += self.headheight+cheight
        ew = self.foot_end.get_width()
        lw = self.bottom_line.get_width()
        screen.blit(self.foot_end,(x,y))
        screen.blit(self.bottom_line,(x+ew,y))
        screen.blit(flip(self.foot_end,True,False),(x+ew+lw,y))

    def get_selected(self):
        return self.selected[1]

    def key_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                i = self.selected[0]-1
                while i >= 0:
                    if self.contents[i].selectable:
                        self.selected = (i,self.contents[i])
                        break
                    i -= 1
            elif event.key == pygame.K_DOWN:
                i = self.selected[0]+1
                while i < len(self.contents):
                    if self.contents[i].selectable:
                        self.selected = (i,self.contents[i])
                        break
                    i += 1

    def mouse_event(self,event):
        pass

    def make_choice(self):
        return self.selected[1].choose()


class Widget(object):
    def __init__(self):
        self.width = 0
        self.height = 0
        self.selectable = False
    def get_surface(self):
        return

    def choose(self):
        return

    def set_master(self,textframe):
        self.master = textframe
    
class SurfWidget(Widget):
    def __init__(self,surface):
        self.surface = surface
        self.width = surface.get_width()
        self.height = surface.get_height()
        self.selectable = False

    def get_surface(self):
        return self.surface

class SpaceWidget(Widget):
    def __init__(self,height):
        self.width = 0
        self.height = height
        self.selectable = False

    def get_surface(self):
        return 
    
class ChoiceWidget(Widget):
    def __init__(self,text,command,size="normal"):
        self.on_surf = typefaces.prepare(text,size=size,colour=(0,0,0))
        self.off_surf = typefaces.prepare(text,size=size,colour=(150,150,150))
        self.command = command
        self.width = self.on_surf.get_width()
        self.height = self.on_surf.get_height()
        self.selectable = True

    def get_surface(self):
        sel = self.master.get_selected()
        if sel == self:
            return self.on_surf
        else:
            return self.off_surf

    def choose(self):
        return self.command
