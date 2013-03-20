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
        add_var("Total Weight", "pounds", INT32, 'TOTAL_WEIGHT')
        
        
def setup_events(add_event):        
    
        
        pass
