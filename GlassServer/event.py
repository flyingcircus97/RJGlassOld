#!/usr/bin/env python
# ----------------------------------------------------------
# event MODULE for GlassCockpit procject RJGlass
# ----------------------------------------------------------
# This module will take the keys that are pressed on the keyboard and take appropriate action.
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

#This modules creates, assigns, and processes the events for the Glass Protocol.
#This module is used for both the server and client.
import PySimConnect
import struct
import logging


class event_obj(object):
	#This is the a Glass Protocol event object. Used in the Glass server client to send events back and forth.
	#This is not to be confused with FSX events through SimConnect, as that is seprate.
	def __init__(self, addr, pack_format, func, multiple): 
		self.addr = addr #Address of event
		self.pack_format = pack_format #Either "f" - float, "i" - int, "I" - for unsigned int.
		self.pack_size = struct.calcsize(pack_format) #Calculates size in bytes.
		self.func = func #This is the function that is called with event value as argument.
		self.multiple = multiple #If False value is sent as arg, If True value is number of times event is sent.
		
	def process_event(self, value):
		if self.multiple: #value is number of times function is called.
			if isinstance(value,int): #Make sure int
				for i in range(value):
					self.func()
			else:
				logging.info("event: Can't process Event %0X as multiple, data not int.", self.addr)
		else:
			self.func(value)		
		
	
class event_c(object):
	
	
	def __init__(self, aircraft):
		self.aircraft = aircraft
		#Creating dict containing all events
		self.dict = self.create_dict()
		self.keys = self.dict.keys()
		
	def exists(self, addr):
		#Will check if addr exists.
		if addr in self.keys:
			return True
		else:
			return False
	
	def size(self, addr):
		if addr in self.keys:
			return self.dict[addr].pack_size
		
			
	def process(self, addr, data):
		#Sets variable, if settible.
		if addr in self.keys:
			e = self.dict[addr]
			#print "EVENT PROCESS %r %r" %(addr, data)
			#Unpack data
			#try:
			value = struct.unpack(e.pack_format, data)[0]
			#print "VALUE = ", value
			e.process_event(value)
			#except:
				#print "ERROR - unpacking/processing Event %0X  %s %r" %(addr,e.pack_format,data)
				
			
		else:
			logging.info("event: Event Obj Not Found - Not Processed by Server %r", %addr)
			#Not an error, as event could not apply to server.
			
		
	def create_dict(self):
		
		dict = {}
			
		def add_event(address, format, func, multiple = False):
			dict[address] = event_obj(address, format, func, multiple)
		#Load up dictinary with all variables.
		aircraft = self.aircraft
		#Speed
		add_event(0xA100, "f", aircraft.HSI.cycle_Bearing1, True)
		add_event(0xA104, "i", aircraft.airspeed.set_bug, False)
		#Nav1 Test
		add_event(0xA600, "f", aircraft.Com_1.set_active_freq, False)
		add_event(0xA601, "f", aircraft.Com_1.set_standby_freq, False)
		add_event(0xA602, "f", aircraft.Com_2.set_active_freq, False)
		add_event(0xA603, "f", aircraft.Com_2.set_standby_freq, False)
		add_event(0xA604, "f", aircraft.Nav_1.set_active_freq, False)
		add_event(0xA605, "f", aircraft.Nav_1.set_standby_freq, False)
		add_event(0xA606, "f", aircraft.Nav_2.set_active_freq, False)
		add_event(0xA607, "f", aircraft.Nav_2.set_standby_freq, False)
		
		
		return dict