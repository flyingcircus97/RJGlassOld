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
        #Flap Index Handle
        add_var("FLAPS HANDLE INDEX","number", INT32, 'FLAP_HANDLE', send=True)
        
        
def setup_events(add_event):        
    
        pass
        
