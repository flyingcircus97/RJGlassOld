#gauge.py
#***********************************************
#GlassClient RJGlass
#gauge.py - parent class of all gauges
#
#***********************************************

import pyglet

class gauge_parent(object):
    
    def __init__(self, name, folder, size, pos):
        #self.win = pyglet.window.Window(width = 1024, height = 768, display=display)
        self.name = name
        self.folder = folder
        self.size = size
        self.pos = pos
        print "PARENT INIT"
        
        
        #@self.win.event
        #def on_draw():
        #    pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
        #    pyglet.gl.glLoadIdentity()
        #    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
        #    ('v2i', (10, 15, 30, 35)))