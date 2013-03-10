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

class alt_setting(object):
    #Used to calculate altimeter setting for each pilot
    def __init__(self, variable, baro, baro_unit, ind_alt):
        self.pres_alt = variable.byName('PRESSURE_ALT')
        self.baro = variable.byName(baro)
        self.baro_unit = variable.byName(baro_unit)
        self.ind_alt = variable.byName(ind_alt)
        
    def convert2inHG(self):
        self.baro.data.value = int(round(self.baro.data.value* 2.953))+1
        if self.baro.data.value > 3200: self.baro.data.value = 3200
        elif self.baro.data.value < 2700: self.baro.data.value = 2700
        
        return self.baro.data.value
        
    def convert2HPA(self):
        self.baro.data.value = int(round(self.baro.data.value* 0.3386))
        if self.baro.data.value > 1084: self.baro.data.value = 1084
        elif self.baro.data.value < 914: self.baro.data.value = 914
        
        return self.baro.data.value
        
    def calc(self):
        #Check unit
        baro = self.baro.data.value
        if self.baro_unit.data.value: #If inHG
            if baro < 2000: #Wrong unit convert
                baro = self.convert2inHG()
            #Calculate offset from pressure alt
            offset = (baro - 2992) * 10
                
        else: #If HPA
            if baro >= 2000: #Wrong unit convert
                baro = self.convert2HPA()
            #Calculate offset from pressure alt
            offset = int((baro - 1013) * 29.41)
        #Apply offset
        self.ind_alt.data.value = self.pres_alt.data.value + offset

class altitude_c(object):
    
        
    def __init__(self,variable):
                
        self.CPTBaro = alt_setting(variable,'CPT_BARO','CPT_BARO_UNIT','CPT_IND_ALT')
        self.FOBaro = alt_setting(variable,'FO_BARO','FO_BARO_UNIT','FO_IND_ALT')
        
    def test(self):
        pass
        
    def comp(self):
        #Computations per frame
        #Calculate altitude
        self.CPTBaro.calc()
        self.FOBaro.calc()


    
class data(object):

    
    def __init__(self, variable):
        
        self.variable = variable
                
        self.altitude = altitude_c(variable)
            
            
    def comp(self,dt):
        #Client is true, if RJGlass is in client or test mode.
        #global_time = globaltime.value
        #Computer delta_t = Time between last comp and this one
                    
        self.altitude.comp()
        
            
    def comp_second(self,dt):
        
        pass
    
            
    def test(self):

        pass
        
