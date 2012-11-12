"""
GlassData.py

Used the setup data for F16Glass interface to X-Plane.

"""
import os, time
import struct
from XPLMDataAccess import *
from XPLMUtilities import XPLMCommandKeyStroke, XPLMCommandOnce, XPLMCreateCommand

class data_obj(object):
	""" Data object for F16Data 
	"""

	def set_read_write_fun(self, data_read_fun, data_write_fun):
			self.data_read_fun = data_read_fun
			self.data_write_fun = data_write_fun

	def set_lambda(self, func):
			self.lambda_func = func
	
	def __init__(self, data_s, pack_string, lambda_func, offset, type = None):

		self.lambda_func = lambda_func
		self.data_s = data_s
		self.pack_string = pack_string
		self.data_ref = XPLMFindDataRef(data_s)
		self.offset = offset
		self.type = type
		self.prev_value = None
		self.value = None
		if self.data_ref == None:
			print "ERROR: DATA REF NOT FOUND ****" , data_s
		#time.sleep(3.1)
		if pack_string == 'f':
			if offset == None:
				self.set_read_write_fun(XPLMGetDataf, XPLMSetDataf)
			else:
				self.set_read_write_fun(XPLMGetDatavf, XPLMSetDatavf)
		elif pack_string == 'i':
			if offset == None:
				self.set_read_write_fun(XPLMGetDatai, XPLMSetDatai)
			else:
				self.set_read_write_fun(XPLMGetDatavi, XPLMSetDatavi)
		#Type
		if type == 	'TOGGLE':
			self.toggle_count = 0
	
	def read(self):
		#self.prev_value = self.value
		if self.offset == None:
			self.value = self.data_read_fun(self.data_ref)
			return self.value
		else:
			#This will only read one value
			temp_list = []
			self.data_read_fun(self.data_ref, temp_list, self.offset, 1)
			self.value = temp_list[0]
			return temp_list[0]
		
	def lambda_read(self):
	#Includes lambda function
		if self.lambda_func != None:
			return self.lambda_func(self.read())
		else:
			return self.read()
		
	def set(self, value):
		if self.type == 'TOGGLE':
			self.set_toggle(value)
		elif self.type == 'BUTTON':
			self.press_button(value)
		elif self.type == 'COMMAND':
			self.do_command(value)
		elif self.type == 'ONCHANGE':
			self.on_change(value)
		else:
			self.lambda_set(value)
			
	def set_toggle(self, value):
		#Toggle type input
		print "TOGGLE", self.prev_value
		if self.prev_value != None: #Not first time so valid change.
			if self.prev_value != value:
				print "READ", self.read()
				v = self.lambda_func(self.read())
				self.set_value(v) #Toggle function, pass in difference for number of toggles.
				print "TOGGLEING", v 
				#XPLMCommandKeyStroke(0)	
					
				#Since value changed now set value
		self.prev_value = value
	def on_change(self, value):
		print "ON CHANGE", self.prev_value
		if self.prev_value != None: #Not first time so valid change.
			if self.prev_value != value:
				#v = self.lambda_func(self.read())
				self.set_value(value) #Toggle function, pass in difference for number of toggles.
				
				#XPLMCommandKeyStroke(0)	
					
				#Since value changed now set value
		self.prev_value = value
		
	def press_button(self, value):
		if self.prev_value != None: #Not first time so valid change.
			if self.prev_value != value:
				#self.set_value(value) #Toggle function, pass in difference for number of toggles.
				print "KEY PRESS COMMAND"
				XPLMCommandKeyStroke(self.lambda_func(value))
				#XPLMCommandKeyStroke(0)
				#mike = XPLMCreateCommand("sim/operation/reset_flight","Reset Flight")					
				#XPLMCommandOnce(mike)			
				#Since value changed now set value
		self.prev_value = value
	
	def do_command(self, value):
		if self.prev_value != None: #Not first time so valid change.
			if self.prev_value != value:
				#self.set_value(value) #Toggle function, pass in difference for number of toggles.
				print "DO COMMAND"
				#XPLMCommandKeyStroke(self.lambda_func(value))
				#XPLMCommandKeyStroke(0)
				mike = XPLMCreateCommand(self.lambda_func(value),"Reset Flight")					
				XPLMCommandOnce(mike)			
				#Since value changed now set value
		self.prev_value = value	
		

	def set_value(self, value):
		if self.offset == None:
			self.data_write_fun(self.data_ref, value)
		else:
			self.data_write_fun(self.data_ref, value, self.offset, 1)
			
				
	
	def lambda_set(self, value):
		if self.lambda_func != None:
			self.set_value(self.lambda_func(value)) #Trick as in buttons lambda func always return button ID
		else:
			self.set_value(value)
		

class data_list(object):

	def __init__(self, id, file_name = None):
		self.list = []
		self.id = id
		self.pack_string = ''
		if file_name != None:
			self.file_name = os.path.join(os.getcwd(),'Resources','plugins','PythonScripts',file_name)
			#rint self.file_name
			self.load_var()

	def load_var(self):
		f = open(self.file_name,'r')
		for line in f:
			l = line.split(',')
			if len(l)==3:
				print l[0],l[1]
				self.add(l[0],l[1])

	def add(self, addr, data_s, lambda_func= None, offset = None): #Add variable to list
		self.list.append(data_obj(addr, data_s, lambda_func, offset))
		self.pack_string += data_s #Overall pack string
		
	def add_in(self, addr, data_s, type, lambda_func = None, offset = None):
		self.list.append(data_obj(addr, data_s, lambda_func, offset, type))
		self.pack_string += data_s
		
	def make_data_string(self):
		#Used for output data lists.
		s = struct.pack('c',str(self.id)) #Put id in front''
		#s = ''
		#rint self.id
		for item in self.list:
			value = item.lambda_read()
			s += struct.pack(item.pack_string, value)
			
		return s

	def parse_data_in(self, data_in):
		#Used for input data lists.
		ok = False
		try:
			l = struct.unpack(self.pack_string, data_in)
			ok = True
			#print l
		except:
			print "Error parsing data_in"
			return False
		index =0
		for item in self.list:
			item.set(l[index])
			index += 1
		return ok
		
	

