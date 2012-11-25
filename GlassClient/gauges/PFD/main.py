#main.py
#***********************************************
#GlassClient RJGlass
#main.py - PFD main guage
#
#***********************************************

import pyglet
from gauge import gauge_parent
import variable
#Gauge specific imports
import AHorizon
import SpeedTape
import Altimeter

class gauge(gauge_parent):
    
    def __init__(self, *args, **kwds):
        
        super(gauge, self).__init__(*args, **kwds)
        self.set_native_size(800,800)
        
        #Init Parts
        self.AHorizon = AHorizon.gauge_c((500,500),(0,0), parent = self)
        self.SpeedTape = SpeedTape.gauge_c((150,500),(-325,0), parent= self)
        self.Altimeter = Altimeter.gauge_c((185,500),(345,0), parent = self)
        #Init Variables
        
        
        
    def on_draw(self):
            
            self.init_gauge()
            self.draw_border()
            self.AHorizon.on_draw()
            self.SpeedTape.on_draw()
            self.Altimeter.on_draw()
            #self.SpeedTape.draw_border()
            self.end_gauge()
            