from pygame.transform import flip,scale

import chromographs
import typefaces

class TextBox(object):
    head_end = chromographs.obtain("flourish/top-end.png")
    head_mid = chromographs.obtain("flourish/top-mid.png")
    head_line = chromographs.obtain("flourish/top-line.png")
    foot_end = chromographs.obtain("flourish/bottom-end.png")
    foot_line = chromographs.obtain("flourish/bottom-line.png")
    
    def __init__(self,position,text_or_surface,width,
                 fontsize="normal",colour=(0,0,0)):
        self.position = position
        try:
            self.passage = typefaces.prepare_passage(
                text_or_surface,width,size=fontsize,colour=colour)
        except AttributeError:
            self.passage = text_or_surface
        self.prepare_size(width)

    def prepare_size(self,asked_width):
        he = self.head_end
        hl = self.head_line
        hm = self.head_mid
        fe = self.foot_end
        fl = self.foot_line
        self.min_header_width = mhw = he.get_width()*2 + hm.get_width()
        self.min_footer_width = mfw = fe.get_width()*2
        self.width = max(asked_width,self.passage.get_width(),mhw,mfw)
        topgap = (self.width-self.min_header_width)/2
        bottomgap = self.width-self.min_footer_width
        self.top_line = scale(hl,(topgap,hl.get_height()))
        self.bottom_line = scale(fl,(bottomgap,fl.get_height()))
        self.headheight = he.get_height()
        self.footheight = fe.get_height()
        self.indent = (self.width - self.passage.get_width())/2

    def render(self,screen):
        x,y = self.position
        self.render_header(screen)
        screen.blit(self.passage,(x+self.indent, y+self.headheight))
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
        y += self.headheight+self.passage.get_height()
        ew = self.foot_end.get_width()
        lw = self.bottom_line.get_width()
        screen.blit(self.foot_end,(x,y))
        screen.blit(self.bottom_line,(x+ew,y))
        screen.blit(flip(self.foot_end,True,False),(x+ew+lw,y))
