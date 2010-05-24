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

class airspeed_c(object):
	
	def set_disp(self, Vspeed):
		#This sets what is displayed below speed tape. (Goes blank after a few seconds)
		self.Vspeed_disp = Vspeed

		
		
	def cycle_Vspeed_input(self):
		temp = self.Vspeed_input
		if temp == self.V1:
			out = self.VR
		elif temp == self.VR:
			out = self.V2
		else:
			out = self.V1
		self.Vspeed_input = out
		self.set_disp(out)
					
	def inc_Vspeed_input(self):
		self.Vspeed_input.inc()
		self.set_disp(self.Vspeed_input)
		
	def dec_Vspeed_input(self):
		self.Vspeed_input.dec()
		self.set_disp(self.Vspeed_input)
		
	def visible_Vspeed_input(self):
		self.Vspeed_input.onoff()
		self.set_disp(self.Vspeed_input)
		
	def inc_VT(self):
		self.VT.inc()
		self.set_disp(self.VT)
	def dec_VT(self):
		self.VT.dec()
		self.set_disp(self.VT)
		
	def visible_VT(self):
		self.VT.onoff()
		self.set_disp(self.VT)
	
	def set_bug(self, value):
		self.bug.set_value(value)
		
	
	def __init__(self,variable):
		self.IAS = variable.byName('IAS').data #self.IAS.value is value read from FSX
		self.IAS_guage = 40.0
		self.IAS_diff = 10.0 #Pink Line to show accel or decell
		self.trend_visible = False #Speed trend turns on  H> 20ft, turns off speed <105kts
		self.IAS_prev = self.IAS.value
		self.IAS_list = [0] * 40 # This is used to compute IAS accelertation for airspped tape
		self.TAS = 0.0
		self.Mach = variable.byName('Mach').data
		self.Mach.active = False
		self.GS = variable.byName('GS').data
		#self.V1 = V_speed_c("V1 ", 135)
		#self.V2 = V_speed_c("V2 ", 144)
		#self.VR = V_speed_c("VR ", 137)
		#self.VT = V_speed_c("VT ", 110)
		#self.Vspeed_input = self.V1  #Currently selected one to be changed by knob
		#self.Vspeed_disp = self.V1 #The one that is displayed below speed tape
		#self.Vspeed_disp_timer = 0 #Used for delay of timer
		self.bug = variable.byName('IAS_Bug').data
		self.maxspeed = 260 #Never Exceed speed Red line
		self.minspeed = 220 #Stall speed
		self.lowspeed = 140
		
	def test(self):
		self.IAS_guage += 0.2
		
	def comp(self):
		#Comput the data for airspeed
		#self.IAS.
		if self.IAS.value <=40:
			self.IAS_guage = 40
		else: 
			self.IAS_guage = self.IAS.value

	def comp_IAS_accel(self, airspeed, frame_rate):
		#Computes forcastes IAS in 10 seconds for the IAS tape IAS_diff
		#Find difference between new_IAS and last reading
		diff = self.IAS.value - self.IAS_prev
		self.IAS_prev = self.IAS.value
		#Add diff reading to list pop oldest one
		self.IAS_list.append(diff)
		self.IAS_list.pop(0)
		a= self.IAS_list
		self.IAS_diff = (sum(a) / len(a)) / frame_rate * 10


class data(object):

	
	def __init__(self, variable):
		
		self.variable = variable
				
		self.airspeed = airspeed_c(variable)
			
			
	def comp(self):
		#Client is true, if RJGlass is in client or test mode.
		#global_time = globaltime.value
		#Computer delta_t = Time between last comp and this one
					
		self.airspeed.comp()
		
			
	def comp_second(self):
		
		pass
	
			
	def test(self):

		#time.sleep(0.01)
		self.airspeed.IAS.value += 1
		
		