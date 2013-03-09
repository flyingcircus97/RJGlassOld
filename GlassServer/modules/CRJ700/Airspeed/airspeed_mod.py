#!/usr/bin/env python
# ----------------------------------------------------------
# aircraft_data MODULE for GlassCockpit procject RJGlass
# ----------------------------------------------------------
# This module handels and stores all aircraft data, and communicated via Simconnect to FSX
#
# Copyright 2007 Michael LaBrie
#
#    This file is part of RJGlass.
#
#    RJGlass is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.

#   RJGlass is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# test mod for CVS
# ---------------------------------------------------------------


import time
import variables.valid_check as valid_check
import config

class airspeed_c(object):
    
        
    def __init__(self,variable):
                
        self.flap_speed = config.general.config['VSpeeds']['flap_speed']
        self.pusher_multi = config.general.config['Pusher']['flap_multi']
        self.pusher_offset = config.general.config['Pusher']['flap_offset']
        self.max_speed = variable.byName('MAX_CUE')
        self.min_speed = variable.byName('MIN_CUE')
        self.flap_pos = variable.byName('FLAP_HANDLE')
        self.total_weight = variable.byName('TOTAL_WEIGHT')
        self.on_ground = variable.byName('ON_GROUND')
        self.min_cue_timer = 0.0
        
    def test(self):
        pass
        
    def comp(self,dt):
        #Computations per frame
        #try:
        flap_pos = self.flap_pos.getvalue()
        self.max_speed.data.value = int(self.flap_speed[flap_pos])
        #Pusher speed is calculated by linear equation, using weight of plane and flap configuration ONLY
        if self.on_ground.data.value:
            self.min_cue_timer = 0.0
            self.min_speed.data.value = 0 #Disable since on ground
        else: #In Air
            self.min_cue_timer += dt
            if self.min_cue_timer >= 3.0:
                pusher_speed = self.total_weight.data.value*float(self.pusher_multi[flap_pos])+float(self.pusher_offset[flap_pos])
                self.min_speed.data.value = int(pusher_speed * 1.05)+1
                self.min_cue_timer = 3.0 #So doesn't overflow
            
        #except:
        #    pass


    
class data(object):

    
    def __init__(self, variable):
        
        self.variable = variable
                
        self.airspeed = airspeed_c(variable)
            
            
    def comp(self,dt):
        #Client is true, if RJGlass is in client or test mode.
        #global_time = globaltime.value
        #Computer delta_t = Time between last comp and this one
                    
        self.airspeed.comp(dt)
        
            
    def comp_second(self,dt):
        
        print "SECOND"
    
            
    def test(self):

        pass
        
