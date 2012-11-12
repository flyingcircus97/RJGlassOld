#!/usr/bin/env python
# ----------------------------------------------------------
# FSX Definitions 
# ----------------------------------------------------------
from common import *#DataTypes


def setup(add_var):
        
        #add_var("Plane Latitude", "degrees", FLOAT32, 'PLANE_LAT', send = True)
        #add_var("Plane Longitude", "degrees", FLOAT32, 'PLANE_LONG', send = True)
        #add_var("Plane Altitude", "feet", INT32, 'PLANE_ALT', send = True)
        #add_var("Plane Heading Degrees Magnetic", "degrees", FLOAT32, 'PLANE_HDG_MAG', send = True)
        #add_var("Plane Heading Degrees True", "degrees", FLOAT32, 'PLANE_HDG_TRUE', send = True)
        add_var("Plane Bank Degrees" , 'f', 'PLANE_BANK')
        #add_var("Plane Pitch Degrees" , 'f', 'PLANE_PITCH', lambda x:-x, lambda x:-x)
        add_var("Plane Pitch Degrees" , 'f', 'PLANE_PITCH')
        #add_var("Vertical Speed" , "ft/min", FLOAT32, 'VERT_SPEED')
        #add_var("SIM ON GROUND", "", INT32, 'ON_GROUND', converttoBool)
     
        
def setup_events(add_event):        
    
        
        pass