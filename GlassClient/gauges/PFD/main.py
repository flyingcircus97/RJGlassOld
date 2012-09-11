#gauge.py
#***********************************************
#GlassClient RJGlass
#gauge.py - parent class of all gauges
#
#***********************************************

import pyglet
from gauge import gauge_parent

class gauge(gauge_parent):
    
    def __init__(self, *args, **kwds):
        print "TEST"
        super(gauge, self).__init__(*args, **kwds)
        
        print self.name
        
    def on_draw(self):
            pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
            pyglet.gl.glLoadIdentity()
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
            ('v2i', (10, 15, 30, 35)))