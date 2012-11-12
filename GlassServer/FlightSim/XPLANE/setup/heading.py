#!/usr/bin/env python
# ----------------------------------------------------------
# FSX Definitions 
# ----------------------------------------------------------
from common import *#DataTypes


def setup(add_var):
        #Heading
        add_var("TURN COORDINATOR BALL", "Position 128", INT32,  'TURN_CORD')
        add_var("Heading Indicator", "degrees", FLOAT32, 'MAG_HEAD_IND')
        add_var("MAGVAR", "degrees", FLOAT32, 'MAG_VARIATION')
        add_var("GPS GROUND MAGNETIC TRACK", "degrees", FLOAT32, 'MAG_TRACK')
        
def setup_events(add_event):        
    
        
        pass