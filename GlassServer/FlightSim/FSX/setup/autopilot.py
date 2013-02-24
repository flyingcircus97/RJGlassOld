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
        #Autopilot
        add_var("AUTOPILOT ALTITUDE LOCK VAR","feet", INT32, 'ALT_BUG', send=True)
        add_var("AUTOPILOT HEADING LOCK DIR","degrees", INT32, 'HDG_BUG', send=True)
        
def setup_events(add_event):        
    
        
        add_event('HEADING_BUG_SET', 'HDG_BUG') 
        add_event('AP_ALT_VAR_SET_ENGLISH', 'ALT_BUG')
