#!/usr/bin/env python
# ----------------------------------------------------------
# FSX Definitions 
# ----------------------------------------------------------
#DataTypes
INT32 = 1
INT64 = 2
FLOAT32 = 3
FLOAT64 = 4
STRING8 = 5
STRING32 = 6
STRING64 = 7
STRING128 = 8
STRING256 = 9

    

def setup(add_var):
        #Airspeed
        add_var("Airspeed Indicated", "knots", FLOAT32, 'IAS', send = True)
        add_var("Airspeed True", "knots", FLOAT32, 'TAS', send = True)
        add_var("GROUND VELOCITY", "knots", FLOAT32, 'GS')
        add_var("Airspeed Mach", "mach", FLOAT32, 'MACH')
        
def setup_events(add_event):        
    
        
        pass
