#gauge.py
#***********************************************
#GlassClient RJGlass
#gauge.py - parent class of all gauges
#
#***********************************************

import pyglet
import text

class gauge_parent(object):
    
    def __init__(self, size, pos, name = None, folder = None, parent = None):
        #self.win = pyglet.window.Window(width = 1024, height = 768, display=display)
        self.name = name
        if self.name:
            self.name_x = len(self.name)*6 #Used for offset to center name on gauge
        else:
            self.name_x = 0
        self.folder = folder
        self.size = size
        self.size_div2 = map(lambda x: x/2, self.size)
        self.pos = pos
        self.parent = parent
        
        self.native_size = None
        self.scale_x = 1.0
        self.scale_y = 1.0
        
        if parent:
            self.parent_scale_lw = parent.scale_lw
        else:
            self.parent_scale_lw = 1.0
        
        
    def set_native_size(self, x, y):
        self.native_size = (x,y)
        self.native_size_div2 = map(lambda x: x/2, self.native_size)
        self.calc_scale()
        
    def calc_scale(self):
        #Calculate x and y scale factor
        self.scale_x = 1.0 * self.size[0] / self.native_size[0]
        self.scale_y = 1.0 * self.size[1] / self.native_size[1]
        #Calcuate scale factor for Linewidth
        # -- Use average for time being, see how it results. Feeling aspect ratio of gagues will stay consistant
        self.scale_lw = ((self.scale_x + self.scale_y) / 2.0) * self.parent_scale_lw
        #self.scale_x = 1.0
        #self.scale_y = 1.0
        #print self.scale_x, self.scale_y
        #print self.size
        #print self.native_size
        
    def draw_border(self):
        #Draws border along with name of gauge
        pyglet.gl.glColor3f(1.0,0.0,0.0)
        x = self.native_size_div2[0]
        y = self.native_size_div2[1]
        pyglet.graphics.draw(4, pyglet.gl.GL_LINE_LOOP, ('v2i', (-x,-y,-x,y,x,y,x,-y)))
        #Draw name of gauge
        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslatef(-self.name_x,(y-15),0)
        pyglet.gl.glScalef(0.16,0.16,1.0)
        text.write(self.name)
        pyglet.gl.glPopMatrix()
        
    def init_gauge(self):
        #Initalizes position of guage scaling and translation
        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslatef(self.pos[0],self.pos[1],0)
        pyglet.gl.glScalef(self.scale_x,self.scale_y,0)
        
        #@self.win.event
        #def on_draw():
        #    pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
        #    pyglet.gl.glLoadIdentity()
        #    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
        #    ('v2i', (10, 15, 30, 35)))
        
    def darken(self, brightness=255):
        if brightness<255:
            
            pyglet.gl.glColor4f(0.0,0.0,0.0,1-(brightness/255.0))
            x = self.native_size_div2[0]
            y = self.native_size_div2[1]
            pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON, ('v2i', (-x,-y,-x,y,x,y,x,-y)))
        
    def end_gauge(self):
        
        pyglet.gl.glPopMatrix()
        
    def on_draw(self, draw_border = False):
        self.init_gauge()
        self.draw()
        if draw_border: self.draw_border()
        
        self.end_gauge()
        
    def linewidth(self):
        #Compensates linewidth for scale_x and scale_y
        return(self.scale_lw)
    
    def glLineWidth(self, w):
        pyglet.gl.glLineWidth(self.scale_lw*w)
        
