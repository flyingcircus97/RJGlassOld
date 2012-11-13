#!/usr/bin/env python
# ----------------------------------------------------------
# FSX Definitions 
# ----------------------------------------------------------
from common import *

def setup(add_var):
        #Airspeed
        add_var("Radio Height", "feet", INT32, 'RADAR_ALT')
        add_var("Indicated Altitude", "feet", INT32, 'IND_ALT')
        add_var("Pressure Altitude", "feet", INT32, 'PRESSURE_ALT')
        add_var("Kohlsman Setting HG", "inHG", FLOAT32, 'ALT_SETTING')
        
        
def setup_events(add_event):        
    
        add_event('KOHLSMAN_SET', 'ALT_SETTING', lambda x:int(x*16*33.864)) #Convert from inHG to milibars * 16
                
