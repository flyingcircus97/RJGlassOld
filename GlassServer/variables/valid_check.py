#!/usr/bin/env python
# ----------------------------------------------------------
# valid MODULE for GlassCockpit procject RJGlass
# ----------------------------------------------------------
# 
#
# Copyright 2009 Michael LaBrie
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
# ---------------------------------------------------------------

class within(object):
    #Valid if number within >= min and <= max
    def __init__(self, min, max):
        self.min = min
        self.max = max
    def test(self, value):
        
        if (self.min <= value <= self.max):
            return value
        else:
            return None
        
class roundto(object):
    #Round to the nearest (For Nav/Com Radios) exmaple 0.05 for Nav.
    def __init__(self, nearest):
        self.nearest = nearest
    def test(self, value):
        #print "VALUE" , value
        #temp = round(1.0 * value / self.nearest) * self.nearest
        
        return round(1.0 * value / self.nearest) * self.nearest
        


class check_c(object):
    #Object to setup validity check for variables.
    def __init__(self):
        self.objects = [] #list of validity objects
        
    def add_test(self, object):
        self.objects.append(object)
       
    
    def test(self, value):
        #Go through all checks and return value.
        # If value becomes None then value is invalid.
        temp_v = value
        for obj in self.objects:
            if (temp_v != None):
                temp_v = obj.test(temp_v)
                
        #print "RETURN", temp_v
        return temp_v

