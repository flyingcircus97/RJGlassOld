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
import HSI
import VSI
import time

class gauge(gauge_parent):
    
    def __init__(self, *args, **kwds):
        
        super(gauge, self).__init__(*args, **kwds)
        self.set_native_size(1000,1000)
        y = 100
        y2 = -400
        #Init Parts
        self.AHorizon = AHorizon.gauge_c((500,500),(0,y), parent = self)
        self.SpeedTape = SpeedTape.gauge_c((150,500),(-325,y), parent= self)
        self.Altimeter = Altimeter.gauge_c((185,500),(345,y), parent = self)
        self.HSI = HSI.gauge_c((800,500),(0,y2), parent=self)
        self.VSI = VSI.gauge_c((170,300),(335,y2-5), parent=self)
        #Init Variables
        self.DH_notify = False
        #Set up timing
        self.prev_time = time.time()
        
    def calc_dt(self):
        t = time.time()
        dt = t-self.prev_time
        self.prev_time += dt
        
        return dt
    
    def on_draw(self):
            
            self.init_gauge()
            #self.draw_border()
            dt = self.calc_dt()
            self.Altimeter.dt = dt
            self.AHorizon.dt = dt
            self.HSI.dt = dt
            self.AHorizon.on_draw()
            self.SpeedTape.on_draw()
            self.Altimeter.on_draw()
            self.HSI.on_draw()
            self.VSI.on_draw()
            #self.SpeedTape.draw_border()
            self.end_gauge()
            