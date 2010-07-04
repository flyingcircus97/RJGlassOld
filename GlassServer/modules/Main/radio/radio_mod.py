#!/usr/bin/env python
# ----------------------------------------------------------
# aircraft_data MODULE for GlassCockpit procject RJGlass
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


class xpdr_check(object):
	#XPDR specific valid check. Digit from 0000 to 7777
	def test(self, value):
		valid = True
		temp_v = int(value) #Make sure int postitive
		if ((7778 < temp_v) or (temp_v < 0)):
			valid = False
		digits = [temp_v / pow(10,i) %10 for i in range(4)]
				
		for i in digits:
			#If any digit >7 then not valid Transponder Code
			if (i>7):
				valid = False
		
		if valid:
			return value
		else:
			return None

class radio_c(object):
	
		
	def __init__(self,variable):
		self.NAV1_ACTIVE = variable.byName('NAV1_ACTIVE') #self.IAS.value is value read from FSX
		#variable.add_check(valid_check.within(118.000,135.000), ['NAV1_ACTIVE'])
		
		#Set up Valid Checks
		navs = ['NAV1_ACTIVE','NAV1_STANDBY','NAV2_ACTIVE','NAV2_STANDBY']
		variable.add_test(valid_check.within(108.000,117.990), navs)
		variable.add_test(valid_check.roundto(0.05), navs)
		coms = ['COM1_ACTIVE','COM1_STANDBY','COM2_ACTIVE','COM2_STANDBY']
		variable.add_test(valid_check.within(118.000,136.990), coms)
		variable.add_test(valid_check.roundto(0.025), coms)
		adfs = ['ADF1_ACTIVE','ADF1_STANDBY','ADF2_ACTIVE','ADF2_STANDBY']
		variable.add_test(valid_check.within(100.0,1799.99), adfs)
		variable.add_test(valid_check.roundto(0.1), adfs)
		variable.add_test(xpdr_check(),['XPDR'])
		#self.NAV1_ACTIVE.add_test(valid_check.within(118.000,135.000))	
		#self.NAV1_ACTIVE.add_test(valid_check.roundto(0.05))	
	def test(self):
		pass
		
	def comp(self):
		#Computations per frame
		pass

	
class data(object):

	
	def __init__(self, variable):
		
		self.variable = variable
				
		self.radio = radio_c(variable)
			
			
	def comp(self):
		#Client is true, if RJGlass is in client or test mode.
		#global_time = globaltime.value
		#Computer delta_t = Time between last comp and this one
					
		self.radio.comp()
		
			
	def comp_second(self):
		
		pass
	
			
	def test(self):

		#time.sleep(0.01)
		#self.airspeed.IAS.value += 1
		pass
		
