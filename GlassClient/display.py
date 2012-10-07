#display.py
#***********************************************
#GlassClient RJGlass
#display.py  -- Used to initalize the display and windows for pyglet
#
#***********************************************

import os

import pyglet
from pyglet.gl import *
from xml.etree.ElementTree import ElementTree

import gauge

class display_c(object):
    
    def __init__(self, parse_file=None):
    #Initalize the display
    # fullscreen if True, setup fullscreen windows
    # fullscreen if False, setup 1024x768 windows
    
#window = pyglet.window.Window(fullscreen=True)
        self.platform = pyglet.window.get_platform()
        self.display = self.platform.get_default_display()
        self.screens = self.display.get_screens()
        self.parse_file = parse_file
        self.window = None #Leave None for now, will be created in self.parse_xml
        self.fps_display = pyglet.clock.ClockDisplay()
        self.view_l = [] #view list
        
        if parse_file != None:
            
            self.parse_view_xml(parse_file)
        #window_list = []
        #for screen in screens:
        #if fullscreen:
        #    win = pyglet.window.Window(fullscreen=True, display=display)
        #else:
        #    win = pyglet.window.Window(width = 1024, height = 768, display=display)
           
        #window_list.append(win)
        
    def parse_view_xml(self, parse_file):
        
        def xml_val(element, prev=None):
            if element == None:
                return prev
            else:
                return element.text
            
        #Parses xml config file 
        full_parse = os.path.join(os.getcwd(),'views', parse_file)
        #print full_parse
        tree = ElementTree()
        tree.parse(full_parse)
        
        #Create/Adjust window
        config = pyglet.gl.Config(sample_buffers=1, samples=2)
        #Read fullscreen
        if 'Y' == xml_val(tree.find("fullscreen")):
            self.win = pyglet.window.Window(fullscreen=True, display = self.display)
        else:
            size = xml_val(tree.find("size"))
            if size:
                width,height = size.split(",")
                self.win = pyglet.window.Window(width = int(width), height = int(height), display=self.display) 
        #print fs, size_x, size_y
        #Read views
        views = tree.findall('view')
        for view in views:
            view_name = xml_val(view.find('name'))
            view_i = view_c(view_name)
            #Read guages
            gauges = view.findall('gauge')
            for g in gauges:
                #Compute size field (percentage * 100)
                size = xml_val(g.find('size'))
                if size:
                    size = map(lambda x:int(x), size.split(','))
                #Computer pos field (percentage * 100)
                pos = xml_val(g.find('pos'))
                if pos:
                    pos = map(lambda x:int(x), pos.split(','))
                #Folder field
                folder = xml_val(g.find('folder'))
                #name field
                name = xml_val(g.find('name'))
                #Import gauge
                i_name = 'gauges.' + name
                g = __import__(i_name, fromlist=['main'])
                gauge_i = g.main.gauge(size, pos, name,folder)
                #gauge_i = gauge.gauge_c(name,folder,size,pos)
                view_i.appendGauge(gauge_i)
        
        self.view_l.append(view_i)
                
        @self.win.event
        def on_draw():
            pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
            pyglet.gl.glLoadIdentity()
            glEnable(GL_LINE_SMOOTH)
            glEnable(GL_BLEND)
            #glBlendFunc(GL_SRC_ALPHA, GL_ZERO)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
            self.fps_display.draw()
            for g in self.view_l[0].gauges:
                pyglet.gl.glPushMatrix()
                g.on_draw()
                pyglet.gl.glPopMatrix()
                
            
 
class view_c(object):
        #A view is a collection of guages, in a set layout.
        #A display will cycle through  a list of views
        
        def __init__(self,name):
            
            self.name = name
            self.gauges = []
        
        def appendGauge(self, i):
            self.gauges.append(i)
        
    
    
