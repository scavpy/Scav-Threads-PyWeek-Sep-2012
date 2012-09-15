import pygame
from pygame.transform import flip,scale

import chromographs
import typefaces
import facilities
import units
import re
from accounting_mode import lsb

from math import sin, cos, sqrt, radians, pi

WHITE = (255,255,255)
RED = (255,0,0)


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

class PunchCard(object):
    bg = chromographs.obtain("iconic/punchcard.png")
    width = bg.get_width()
    height = bg.get_height()

    def __init__(self, position):
        self.position = position
        self.message = typefaces.prepare("Return key to punch the card",
                                         size="small")
        self.text = ""
        self.update()

    def update(self):
        self.textsurf = typefaces.prepare(self.text+"|")

    def key_event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                return self.text
            elif e.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                char = e.unicode
                if re.match("[A-Za-z ]",char):
                    self.text += char.upper()
            self.update()

    def make_choice(self):
        return self.text

    def mouse_event(self, e):
        return

    def render(self,screen):
        x,y = self.position
        screen.blit(self.bg,(x,y))
        dw = (self.width - self.textsurf.get_width()) / 2
        screen.blit(self.textsurf,(x+dw,y+self.height/2))
        screen.blit(self.message, (x+80,y+self.height-50))

class BuildMenu(object):
    spanner = chromographs.obtain("iconic/spanner.png")
    gear = chromographs.obtain("iconic/wee-gear.png")
    gearrect = gear.get_rect()
    optrad = gearrect.width//2

    def __init__(self, situation):
        self.is_open = False
        self.facs = []
        self.units = []
        self.options = []
        self.position = (0,0)
        self.repairable = None
        self.centerrect = pygame.Rect(0,0,64,64)
        self.situation = situation
        self.pricetag = None

    def open_menu(self,position,repairable=None,edge=False):
        self.repairable = repairable
        self.is_open = True
        x,y = position
        x = min(max(120,x),900)
        y = min(max(120,y),500)
        self.position = (x,y)
        self.centerrect.center = self.position
        if edge:
            self.facs = self.situation.fence_plans
            self.units = []
        else:
            self.facs = self.situation.facility_plans
            self.units = self.situation.unit_plans
        self.options = self.halfwheel(facilities,self.facs,-1)
        self.options.extend(self.halfwheel(units,self.units,1))
        self.options.append((None,None,self.centerrect))
        if repairable:
            rect = self.spanner.get_rect()
            rect.center = (x+self.optrad*2,y)
            self.options.append(("REPAIR",self.spanner,rect))

    def close_menu(self):
        self.repairable = None
        self.is_open = False

    def halfwheel(self,module,items,hemisphere):
        x,y = self.position
        result = []
        numitems = len(items)+1
        d = self.optrad*2
        if numitems > 3:
            r = d+(numitems*5)
        else:
            r = d
        angle = hemisphere * radians(180.0/numitems)
        for i,item in enumerate(items):
            itemclass = getattr(module,item,None)
            img = chromographs.obtain("iconic/%s.png"%item)
            rect = img.get_rect()
            rect.center = (x + -cos(angle*(i+1))*r, y + sin(angle*(i+1))*r)
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
        x,y = self.position
        if self.pricetag:
            if x<500:
                px = x+50
            else:
                px = x-50-self.pricetag.get_width()
            screen.blit(self.pricetag,(px,y+self.optrad*3))

    def mouse_event(self, e):
        px,py = e.pos
        for itemclass,image,rect in self.options:
            x,y = rect.center
            dx,dy = (px-x,py-y)
            dist2 = dx*dx+dy*dy
            if dist2 <= self.optrad*self.optrad:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if itemclass and (itemclass == "REPAIR" or
                                      self.situation.can_afford_a(itemclass)):
                        return itemclass
                elif e.type == pygame.MOUSEMOTION:
                    self.update_pricetag(itemclass)
        return None

    def update_pricetag(self, item):
        text = None
        r = self.repairable
        colour = WHITE
        if item:
            if item == "REPAIR" and r:
                cost = int((float(r.damage)/r.durability)*r.cost)
                price = lsb(cost) if cost>0 else "free"
                text = "Repair %s for %s"%(r.name,price)
                if cost > self.situation.wealth:
                    colour = RED
            elif item.human:
                price = ("for %s"%lsb(item.cost)) if item.cost>0 else ""
                if self.situation.population < 1 or item.cost > self.situation.wealth:
                    colour = RED
                text = "Deploy %s %s"%(item.name,price)
            else:
                price = lsb(item.cost) if item.cost>0 else "free"
                text = "Build %s for %s"%(item.name,price)
                if item.cost > self.situation.wealth:
                    colour = RED
        self.pricetag = typefaces.prepare(text, size="small",
                                          colour=colour)

class StatusBar(object):
    height = 120
    live_ship = chromographs.obtain("iconic/living-ship.png")
    dead_ship = chromographs.obtain("iconic/dead-ship.png")
    gear = chromographs.obtain("iconic/wee-gear.png")
    gearrect = gear.get_rect()
    intensity = 80
    slowness = 4.0

    def __init__(self):
        self.stats_table = None
        self.remaining_ships = 0
        self.max_ships = 0
        self.last_build = None
        self.icon_rect = None
        self.messages = None
        self.unit_name = None
        self.message_stack = []
        self.flashing = 0

    def flash(self,frames):
        self.flashing = frames

    def update(self, money, food, pop, last_build, ships, remaining):
        self.stats_table = typefaces.prepare_table(
            [["Wealth",":  ",lsb(money)],
             ["Food",":  ",str(food)],
             ["Troops",": ",pop]],
            colour = (255,255,255), alignment="llr")
        self.last_build = chromographs.obtain("iconic/%s.png"%last_build.__name__)
        self.icon_rect = self.last_build.get_rect()
        self.remaining_ships = remaining
        self.max_ships = ships

    def push_messages(self, *messages):
        for m in messages:
            if len(self.message_stack) >= 4:
                self.message_stack.pop(-1)
            self.message_stack.insert(0,m)
        self.messages = typefaces.prepare_passage(
            "\n".join(self.message_stack),400,
            colour=(240,240,240), size="small")

    def set_unit_name(self, unit_name):
        if unit_name:
            self.unit_name = typefaces.prepare(unit_name, size="small", colour=(255,255,240))
        else:
            self.unit_name = None

    def render(self,screen,onslaught = False):
        y = screen.get_height() - self.height
        pygame.draw.rect(screen,(0,0,0),(0,y,screen.get_width(),self.height))
        screen.blit(self.stats_table,(20,y+20))
        self.icon_rect.center = (280,y+30)
        self.gearrect.center = (280,y+30)
        screen.blit(self.gear,self.gearrect)
        screen.blit(self.last_build,self.icon_rect)
        for i in range(self.max_ships):
            if i < self.remaining_ships:
                screen.blit(self.live_ship,(700+i*75,y+30))
            else:
                screen.blit(self.dead_ship,(700+i*75,y+30))
        if self.flashing:
            self.flashing -= 1
            glow = int((sin(self.flashing/self.slowness)+1)*(self.intensity/2))
            pygame.draw.rect(screen,(glow,glow,glow),(320,y+20,350,95))
        if self.messages:
            screen.blit(self.messages,(320,y+20))
        if self.unit_name:
            screen.blit(self.unit_name, (self.gearrect.left - 5, self.gearrect.bottom + 5))

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
        self.visible = True

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
        if not self.visible:
            return
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

    def mouse_event(self,event):
        mx, my = event.pos
        x, y = self.position
        y += self.headheight
        for i,c in enumerate(self.contents):
            if c.selectable:
                rect = pygame.Rect(x, y, self.width, c.height)
                if rect.collidepoint(mx, my):
                    self.selected = (i,c)
                    if (event.type == pygame.MOUSEBUTTONDOWN and
                        event.button == 1):
                        return c.command
            y += c.height
        return None

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

class SelfAdvancingScroll(Widget):
    """ A scroll that advances at its own
    pace so as to reveal successive lines of text """

    def __init__(self, text, location, dots_per_second=20):
        self.scroll = typefaces.prepare_passage(text, location.width)
        self.location = location
        self.dots_per_second = dots_per_second
        self.end_position = location.height
        self.end_position = self.scroll.get_height() - location.height
        self.position = -location.height
        self.rate = 1

    def stopped(self):
        return self.rate == 0

    def render(self, screen):
        """ show the part that is visible """
        width, height = self.location[2:]
        peephole = pygame.Surface((width, height), pygame.SRCALPHA)
        peephole.fill((255,255,255,0))
        peephole.fill((0,0,0,32),(0,0,width,8))
        peephole.fill((0,0,0,32),(0,height-8,width,8))
        peephole.fill((0,0,0,64),(0,0,width,4))
        peephole.fill((0,0,0,64),(0,height-4,width,4))
        position = int(self.position)
        peephole.blit(self.scroll, (0,0), (0, position, self.location.width, self.location.height))
        screen.blit(peephole, self.location)

    def advance(self, milliseconds):
        dots = self.dots_per_second * milliseconds * self.rate / 1000.0
        if self.position <= 0:
            dots = max(dots, 0)
        self.position += dots
        if self.position >= self.end_position:
            self.position = max(self.end_position, 0)
            self.rate = 0

    def advance_rapidly(self):
        self.rate = 3

    def advance_slowly(self):
        self.rate = 1

    def regress_rapidly(self):
        self.rate = -2

    def stop(self):
        self.rate = 0
