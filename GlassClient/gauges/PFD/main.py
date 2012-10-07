#main.py
#***********************************************
#GlassClient RJGlass
#main.py - PFD main guage
#
#***********************************************

import pyglet
from gauge import gauge_parent

#Gauge specific imports
import AHorizon

class gauge(gauge_parent):
    
    def __init__(self, *args, **kwds):
        
        super(gauge, self).__init__(*args, **kwds)
        self.set_native_size(500,500)
        
        #Init Parts
        self.AHorizon = AHorizon.gauge_c((500,500),(0,0))
        
        
    def on_draw(self):
            
            self.init_gauge()
            self.draw_border()
            self.AHorizon.on_draw()
            