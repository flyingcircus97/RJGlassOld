#!/usr/bin/env python
# ----------------------------------------------------------
# XPlane Connect for F16Glass
# ----------------------------------------------------------
# This module handels and stores all aircraft data, and communicated via FSUIPC to FS2004
#
# 
# ---------------------------------------------------------------

import threading 
import time
import logging
import struct
import config
#from socket import *
import socket
#Constants
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
#Header length
HEADER_len = 12

#class data_obj(object):
	#Used to make a object for Definition to link to
#	def __init__(self, value, pack_s):
#		self.value = value
#		self.adjusted = value #Used incase value needs to be adjusted from data inputed from FSX.
#		self.pack_s = pack_s
class empty_event(object):
		
	def send(self):
		logging.debug("Pass, no function associated with this event to do.")

class event_obj(object):
	#Used to hold send event, with its data
	def __init__(self,value):
		self.value = value
		self.event_id = 0 #Set for 0 initially, will be equal to index of event list for this object
		self.event = empty_event()


class XPlaneUDP_Client_c(threading.Thread):
	
	def __init__(self, recieve):
		self.clock = time.time()
		self.count = 0
		self.kill_timer = 0
		threading.Thread.__init__(self) 
		self.started = False
		self.read_buffer = ''
		self.packet_data = []
		self.go = True
		self.recieve = recieve
		
	def reset(self):
		self.count = 0
		self.kill_timer = 0
		self.read_buffer = ''
		self.packet_data=[]
		
	def send(self, data):
		#Send to server UDP
		self.s.sendto(data, self.addr)
		logging.debug("UDP OUT: %s %r", data, self.addr)
	
	def start_client(self):
		if self.started==False:
			logging.info("XPlaneConnect: Starting Thread")
			self.start()
			self.started=True
	
	def connect(self, addr, port):
	#Attempts to connect to XPLANE.
		
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		#self.s.settimeout(config.timeout)
		#self.s.connect((addr, port))
		#self.s.setblocking(0)
		self.addr = (addr,port)
		#Send connection header
		#self.s.settimeout(None)
		self.s.settimeout(2)
		#self.s.setblocking(0)
		logging.info("XPlane Connect: Sending Connect string")
		self.send('CONNECT') #The initial connect attempt to XPLANE
		self.connected=True

	def close(self):
		self.go = False
		if hasattr(self, 's'):
			self.s.close()

	def run(self):
		
		def reset_timer():
			#used to reset the kill timer.
			#Called from RJGlass to reset timer, if timer isn't reset then thread will die.
			self.kill_timer = 0
		
		def decode_data(length, packet_type):
			#Used to look for and read anydata that is coming in.
			#Take data from buffer minus header
			data = self.read_buffer[12:length]
			self.read_buffer = self.read_buffer[length:]
			#print "%r" %data
			self.packet_data.append([packet_type, data]) 
			#print "PD", self.packet_data
			return len(self.packet_data)
		
			#print self.packet_data
		#Begin self.receive()
		self.go = True
		logging.info("XPlaneConnect: Server Starting")
		while self.go:
			#print "SERVER LOOP"
		#print time.time()-self.clock
			#try:
			if self.recieve:
				try:
					r, addr2 = self.s.recvfrom(1024)
					logging.debug("UDP RECV (%d) %r ", len(r), r)
				except socket.timeout:
					r = ''
					logging.debug("UDP RECV Timedout")
					
			else:
				r = ''
			#r =self.s.recv(1024)
			#print "%r" %r
			#self.read_buffer = self.read_buffer + r
			self.read_buffer = r
			logging.debug("Recived Buffer (%d) %r", len(r), r)
			#except:
			#	pass
			#self.kill_timer += 1 #This is used to kill thread, if RJGlass crashes, or locks up.
			#if self.kill_timer>200:
			#	self.go = False
		#	print "Error: No Data to Recieve"
				
			#l = len(self.read_buffer)
			#while l>=12: #If not atleast 12bytes than no buffer.
		#		out = decode_header(self.read_buffer)
		#		if out[1]== self.protocol: #Check to see if protocol is correct
		#			status = True #Used in return value
					#print "Header ", out
		#			if l>=out[0]: #Make sure buffer is large enough for entire data
		#				num = decode_data(out[0], out[2]) #The length and type is send to decode data
						#print time.time(), "Packet" , out[0]
		#				l = len(self.read_buffer)
		#				if num > 130: #If data is not being read then close thread.
						#This is so the thread wont run forever.
		#					self.go = False
		#					print "RJGlass is not reading input buffer, exiting client thread."
						#If data is decoded it will be sent to self.packet_data list.
						#print time.time()-self.clock, out[0], out[2]
		#			else:
		#				print self.app_name, "Error: Length not correct" , l, out[0]
		#				l=0 #bad data forces while loop to exit
		#		else: #If protocol wrong then error in transmission clear buffer
					#self.read_buffer = ''
		#			l=0 #forces loop to exit
		#			print self.app_name, "Error in Data: Protocol Wrong,  Read_Buffer cleared" , out[1]
			#print time.time(), "PD < 12"
			#Check read buffer
			#print "%r" %self.read_buffer
			#print "Break"
			#time.sleep(3)
			#Quit thread
		self.s.close()

class XPdata_obj(object):
	
	def __init__(self, var, func=None):
		self.var = var
		self.func = func

class outdata_c(object):
	#Outdata is data sent from XPlane to GlassServer
	#This provides group of outdata
	def __init__(self):
		self.list = []
		self.outpack_s = ''
		self.outpack_size = 0
	def add(self, addr, data_s, obj, func):
		
		self.list.append(XPdata_obj(obj, func))
		self.outpack_s += data_s #Overall pack string
		self.outpack_size = struct.calcsize(self.outpack_s)		
		#print self.outpack_size	
		
class XPlaneUDP(object):
	
	
	def __init__(self, recieve):
		#Initalizes SimConnect
		#Depending on your FSX_version you are connecting to, need to set protocol etc.
#		self.read_buffer = ''
		#Set outdata as two groups High Priority, Low Priority
		self.HP_outdata = outdata_c()
		self.LP_outdata = outdata_c()
		#self.outdata = [self.HP_oudata, self.LP_outdata]
		
		self.connected = False
		#self.aircraft = aircraft
		self.indata_list = []
		self.inpack_list = []
					
		self.client = XPlaneUDP_Client_c(recieve)
		self.data_list = [] #Sets up data list will be object eventually

	def connect(self, addr, port, connect):
		
		
		self.client.connect(addr,port)
		if connect: self.client.start_client()
		self.connected = True
	
	def close(self):
		#Closes the connection with XPlane
		self.client.close()
	
	def send_data(self):
		out_s = ''
		index = 0
		for item in self.indata_list:
			out_s += struct.pack(self.inpack_list[index],item.value)
			index += 1
		self.client.send(out_s)
		logging.debug("XPlaneConnect: Client Out %r", out_s)
		
	def receive(self):
		
		def unpack_data(outdata,data):
		
				out = struct.unpack(outdata.outpack_s, data[1:])
				#print out
				count = 0 
				#print out
				for item in outdata.list:
					#print count, out[count]
					#Possible functio here?
					item.var.client_set(out[count])
					count += 1
		
		def decode_data(data):
					
			id = struct.unpack('c', data[0])
			logging.debug("XPlaneConnect: ID %s received", id[0])
			if id[0] == '1': #High Priority outdata
				#Main Data struct
				unpack_data(self.LP_outdata, data)
				
				
					
			elif id[0] == '2':
				#print "ID 2"		
				pass
						
			
		status = False	#Check packet data to see if any data is in there.
		logging.debug("XPlaneConnect : Readbuffer %d %r", len(self.client.read_buffer), self.client.read_buffer)
		#print self.LP_outdata.outpack_size
		if len(self.client.read_buffer) == self.LP_outdata.outpack_size + 1:
			#print "Decoding Packet", len(self.client.packet_data)
			#print len(self.client.read_buffer), "%r" %self.client.read_buffer
			status = True
			decode_data(self.client.read_buffer)
			#print "R BUFFER %r " %self.client.read_buffer
			self.client.read_buffer = ''
		else:
			pass #print "WRONG SIZE", len(self.client.read_buffer)
			#define_id.append(decode_packet(self.client.packet_data.pop(0)))
		return status
	
	def output(self):
		while len(self.client.packet_data) >0:
			i = self.client.packet_data.pop(0)
			logging.debug("XPlaneConnect: Packet Recv : %d %r", len(i[1]),i)
			
			
			
	
	def indata_add(self, addr, data_s, obj):
		
		self.indata_list.append(obj)
		self.inpack_list.append(data_s) #Overall pack string
		#self.inpack_size = struct.calcsize(self.inpack_s)
	
if __name__ == '__main__':
	s = XPlaneUDP(True)
	s.connect('192.168.1.40', 1500, True)
	s.receive()
	#s.Load_Flightplan('DTWCVG')
	clientID = 2
	defineID = 5
	alt = data_obj(200.0)
	ias = data_obj(200.0)
	s.mapClientDatatoID("TestCDataArea2", clientID)
	s.definition_0 = s.create_ClientDataDefinition(defineID)
	s.def1 = s.create_DataDefinition(3)
	s.def1.add("Indicated Altitude", "feet", FLOAT32, alt)
	s.def1.add("Airspeed Indicated", "knots", FLOAT32, ias)
	airspeed = data_obj(0)
	#s.definition_0.add('Airspeed',FLOAT64, airspeed)
	#s.definition_0.add('Airspeed',FLOAT64, alt)
	#s.definition_0.add('Airspeed',FLOAT64, ias)
	s.output()
	
	#Loop
	f = 22.26
	i = 3
	for i in range(10):
		#s.definition_0.request(clientID, 2, ClientDataDefinition.ONCE)
		#s.def1.request(3,DataDefinition.USER, DataDefinition.ONCE, interval = 0)
		s.requestAIData(3, 5000, 2)
		#s.sendClientData(2,5, struct.pack('<ddd', i,f,f))
		#i+=1
		#f+=1.4
	#print airspeed.value
	#s.receive()
	#alt = data_obj(200.0)
	#s.definition_0.add("Indicated Altitude", "feet", FLOAT32, alt)
	#AGL = alt.get
		time.sleep(2)
		#s.output()
		s.receive()
		#print s.def1.AI_data
	#s.definition_0.request(4, DataDefinition.USER, DataDefinition.VISUAL_FRAME, interval = 10)
	#while True:
	time.sleep(13)
	s.close()
