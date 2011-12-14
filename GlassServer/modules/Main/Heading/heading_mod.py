#!/usr/bin/env python
# ----------------------------------------------------------
# position_mod MODULE for GlassCockpit procject RJGlass
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



class heading_c(object):
	
		
	def __init__(self,variable):
				
		#variable.add_test(valid_check.within(28.0,32.0), ['ALT_SETTING'])
		pass

	def test(self):
		pass
		
	def comp(self):
		#Computations per frame
		pass

	
class data(object):

	
	def __init__(self, variable):
		
		self.variable = variable
				
		self.heading = heading_c(variable)
			
			
	def comp(self):
		#Client is true, if RJGlass is in client or test mode.
		#global_time = globaltime.value
		#Computer delta_t = Time between last comp and this one
					
		self.heading.comp()
		
			
	def comp_second(self):
		
		pass
	
			
	def test(self):

		pass
		
