#!/usr/bin/env python
# ----------------------------------------------------------
# Common function data types for FSXdef's.
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

def converttoBool(value):
    if value == 0:
        return 0
    else:
        return 1    
