#!/usr/bin/env python
# ----------------------------------------------------------
# Testing for SimConnect
# ----------------------------------------------------------
# This module handels and stores all aircraft data, and communicated via FSUIPC to FS2004
#
# 
# ---------------------------------------------------------------

import threading 
import logging
import time
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
SIMCONNECT_DATA_SET_FLAG_TAGGED = 1
#Header length
HEADER_len = 12

class data_obj(object):
    #Used to make a object for Definition to link to
    def __init__(self, value):
        self.value = value
        self.adjusted = value #Used incase value needs to be adjusted from data inputed from FSX.
        self.sim_event = None
        self.sim_obj = None
        self.inhibit = 0 #Used to postpone reading of data value from sim, when data is written too.
        
    def set_value(self, value):
        logging.debug('Set Value - Data Object %r', value)
        self.value = value
        if self.sim_event != None:
            self.sim_event.send()
            self.inhibit = 4
        elif self.sim_obj != None:
            self.sim_obj.send()
            self.inhibit = 4
            
    def reset(self):
        #Sets sim_event and sim_obj to None so variable won't try to communicate.
        #--Used when mode switches from FSX to Test
        self.sim_event = None
        self.sim_obj = None
        
class empty_event(object):
        
    def send(self):
        logging.debug("Empty Event")


class event_obj(object):
    #Used to hold send event, with its data
    def __init__(self,value):
        self.value = value
        self.event_id = 0 #Set for 0 initially, will be equal to index of event list for this object
        self.update = False #Can be used  to tell when to update data to FSX.
        self.event = empty_event()
        self.send_func = lambda x:x #Will be used in Future to handle differnt sims. (X-Plane, FG)
        
class DataRequest(object):
    #Attempt to store all value as data definition objects
    def __init__(self, count, SimCon, definition, name, unit, obj, type, func=None):
        #Create Data Definition and Add it to 
        #First send via TCP to Simconnect
        self.func = func #Func called to convert FSX data to GlassServer var.
        self.send_func = lambda x:x #Func to convert GlassServer var to FSX data.
        self.value = 0
        self.index = count
        self.obj = obj
        d = struct.pack('<I', definition) + SimCon.string256(name) + SimCon.string256(unit)
        e = d + struct.pack('<iii', type, 0, count)
        SimCon.client.send(e, 0x0c)
        #Comput size
        self.size = 4
        self.type = 'i'
        if type == FLOAT32:
            self.value = 0.0
            self.type = 'f'
        self.SimCon = SimCon
        self.definition = definition
        
    def set_send_func(self, func):
        self.send_func = func
        
    def get(self):
        return self.value
    
    def send(self, object_id = 0): #Default object_id to user aircraft.
        value = self.send_func(self.obj.value)
        logging.debug("PySimConnect Sending %r" , value)
        
        flag = SIMCONNECT_DATA_SET_FLAG_TAGGED
        d = struct.pack('<iiiiii' + self.type, self.definition, object_id, flag, 1, 4+ self.size , self.index, value)

        self.SimCon.client.send(d, 0x10)
        

class SimEvent(object):
    def __init__(self, SimCon, eventid, name, data, send_func = None):
        #Mapit on Simconnect
        d = struct.pack('<I', eventid) + SimCon.string256(name)
        SimCon.client.send(d, 0x04)
        self.SimCon = SimCon
        #self.group_id = groupid
        self.eventid = eventid
        self.data = data
        self.data.sim_event = self
        self.send_func = send_func
    def send(self):
        #print self.eventid, self.data.value
        #print "%r" %self.data
        if self.send_func:
            d = struct.pack('<iiiii', 0, self.eventid, self.send_func(self.data.value), 1, 16)
            logging.debug("PySimConnect Event Send Func %r %r", self.data.value, self.send_func(self.data.value))
        else:
            d = struct.pack('<iiiii', 0, self.eventid, self.data.value, 1, 16)
        logging.debug("PySimConnect Event Send %r", d)
        
        self.SimCon.client.send(d, 0x05)
    

class EventList(object):
        def __init__(self,SimCon):
            self.list=[]
            self.prioirty_list = [] #The id's of events that have just changed will be added here.
            self.group_id = id
            self.SimCon = SimCon
            self.count = 1
            self.cycle_count = 0
            self.cycle_timer = 0
        def add(self, name, data, send_func = None):
            #If auto_update=True, event will be occasionally updated.
            t = SimEvent(self.SimCon, self.count, name, data, send_func)
            data.event_id = len(self.list) #Get index of where event id will be placed in list
            #if auto_update:
            self.list.append(t) #Add it to end of list
            #self.list.append(SimEvent(self.SimCon, eventid, name))
            data.event = t
            #AddClientEventToNotificationGroup
            #d = struct.pack('<iii', self.group_id, self.count, 0)
            #self.SimCon.client.send(d, 0x07)
            self.count +=1
            #return t
            
        def cycle(self):
            #Cycle through all of the data in this notification one by one, to make sure data is correct
            self.cycle_timer +=1
            if self.cycle_timer  == 5:
                self.cycle_timer = 0
                self.cycle_count += 1
                if self.cycle_count >= len(self.list):
                    self.cycle_count = 0
                self.list[self.cycle_count].send()
                #self.list[0].send()
        def send_updates(self):
            #Scans through group, if any have update = True, then send data to FSX and reset update flag.
            for item in self.list:
                if item.data.update == True:
                    item.data.update = False
                    item.send()
        def set_priority(self, priority):
            d = struct.pack('<ii', self.group_id, priority)
            #self.SimCon.client.send(d, 0x09)
            time.sleep(8)
            
class DataDefinition(object):
    #Period Constants
    NEVER = 0
    ONCE = 1
    VISUAL_FRAME = 2
    SIM_FRAME = 3
    SECOND = 4
    #Object_ID Constants
    USER = 0
    #Flags Constant
    DEFAULT = 0
    DATA_CHANGED = 1
    
    
    
    #Class to store data definition in list
    def __init__(self, SimCon, id):
        self.list=[]
        self.objlist=[]
        self.id = id
        self.unpack_s = '<' #Always little edian
        self.SimCon = SimCon
        self.data_count = 0
    def add(self, name, unit, type, obj, func=None):
        simobj = DataRequest(self.data_count, self.SimCon, self.id, name, unit, obj, type, func)
        
        #print self.id
        obj.sim_obj = simobj
        self.list.append(simobj)
        self.objlist.append(obj)
        #print obj
        #print self.objlist
        #Add apporpriate type to unpack string
        temp = ''
        if type == FLOAT32:
            temp = 'f'
        elif type == FLOAT64:
            temp = 'd'
        elif type == INT32:
            temp = 'i'
        elif type == STRING8:
            temp = '8s'
        else:
            logging.warning("PySimConnect Error Adding %s: Type Not Found", name)
            #raise
        self.unpack_s += temp
        self.data_count +=1
        return simobj
    
    def request(self, request_id, object_id, period, flag =0, orgin =0, interval =0, limit =0):
        #Request Data on SimObject 0xe
        #flag = 2
        d = struct.pack('<iiiiiiii', request_id, self.id, object_id, period, flag, orgin, interval, limit)
        self.SimCon.client.send(d, 0xe)
        logging.debug("PySimConnect: Sending Request %d", request_id)
        
class SimConnect_Client_c(threading.Thread):
    
    def string256(self, s): #Takes a string and returns it padded to 256
        return s.ljust(256, chr(0))
    
    def __init__(self, name, protocol, FSXname, majorversion, minorversion, subversion, recieve):
        self.protocol = protocol
        self.FSX_subversion = subversion
        self.FSX_majorversion = majorversion
        self.FSX_minorversion = minorversion
        self.FSX_name = FSXname
        self.app_name = name
        self.clock = time.time()
        self.count = 0
        self.kill_timer = 0
        threading.Thread.__init__(self) 
        self.read_buffer = ''
        self.packet_data = []
        self.go = True
        self.recieve = recieve
    def attach_header(self, data, protocol, type, num):
        size = len(data)
        t = type | 0xF0000000
        s = struct.pack('<IIII', size + 16, protocol, t, num)
        final = s + data
        return final
    
    def send(self, data, type):
        #Send the data, will add header, type is type of command
        self.count += 1 #increment count, used to just number requests sent to FSX
        mike = self.attach_header(data, self.protocol, type, self.count)
        self.s.send(mike)
        
    
        
    def connect(self, addr, port):
    #Attempts to connect to FSX.
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(config.timeout)
        self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY,1)
        succeed = False
        try:
            self.s.connect((addr, port))
        
        #Send connection header
        #self.s.settimeout(None)
            self.s.settimeout(config.timeout)
        #self.s.setblocking(0)
            name = self.FSX_name[::-1] #The 3 letter name abbriviation is inverted.
            init_string= self.string256(self.app_name) + struct.pack('<IccccIIII', 0, chr(0), name[0], name[1], name[2], self.FSX_majorversion, self.FSX_minorversion, self.FSX_subversion, 0)
        
            self.send(init_string, 0x01) #The initial connect attempt to FSX.
            succeed = True
        except socket.error:
            logging.debug("PySimConnect Socket: Could Not Connect")
        
        return succeed    

    def close(self):
        try: 
            self.s.close()
        except AttributeError:
            logging.debug("PySimConnect Socket: Can't close Socket, Socket doesn't exist.")

    def quit(self):
        logging.info("PySimConnect: Quitting")
        
        if self.recieve: #Kill Thread
            self.go = False
        else:
            self.close() #No thread to kill, just close socket.
        
    def run(self):
        
        def reset_timer():
            #used to reset the kill timer.
            #Called from RJGlass to reset timer, if timer isn't reset then thread will die.
            self.kill_timer = 0
        def decode_header(s):
                #Decode 1st 12 bytes for the header
                #out[0] length of packet out[1] protocol out[2] type of recieve packet
                t = s[:HEADER_len]
                #print "%r" %t
                out = struct.unpack('<III', t)
                #print "Decode Header", out
                return out    
            
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
        logging.info("PySimConnect Server: Starting")
        
        while self.go:
        #print time.time()-self.clock
            #print self.app_name, "RECIEVE"
            if self.recieve:
                try:
                    r = self.s.recv(1024)
                except socket.timeout:
                    if self.go:
                        logging.info("PySimConnect Server: Recieve Timed Out (Will ReTry)")
                        self.go = False
                except: #Unknown error so shutdown server.
                    self.go = False
            else:
                r = ''
            #r =self.s.recv(1024)
            #print "%r" %r
            #self.read_buffer = self.read_buffer + r
            self.read_buffer = r
            #print "Recived Bytes", len(r)
            #except:
            #    pass
            #self.kill_timer += 1 #This is used to kill thread, if RJGlass crashes, or locks up.
            #if self.kill_timer>200:
            #    self.go = False
        #    print "Error: No Data to Recieve"
                
            l = len(self.read_buffer)
            while l>=12: #If not atleast 12bytes than no buffer.
                out = decode_header(self.read_buffer)
                if out[1]== self.protocol: #Check to see if protocol is correct
                    status = True #Used in return value
                    #print "Header ", out
                    if l>=out[0]: #Make sure buffer is large enough for entire data
                        num = decode_data(out[0], out[2]) #The length and type is send to decode data
                        l = len(self.read_buffer)
                        if num > 4: #If data is not being read then close thread.
                        #This is so the thread wont run forever.
                            self.go = False
                            logging.warning("PySimConnect: Input buffer not being read, exiting client thread.")
                        #If data is decoded it will be sent to self.packet_data list.
                        #print time.time()-self.clock, out[0], out[2]
                    else:
                        logging.warning("PySimConnect Error: Read buffer Length not correct %r %r" , l, out[0])
                        l=0 #bad data forces while loop to exit
                else: #If protocol wrong then error in transmission clear buffer
                    #self.read_buffer = ''
                    l=0 #forces loop to exit
                    logging.warning("PySimConnect Error: Read Buffer Protocol Wrong,  Read_Buffer cleared %r" , out[1])
                    
            
            #Check read buffer
            #print "%r" %self.read_buffer
            #print "Break"
            #time.sleep(3)
            #Quit thread
        self.s.close()
        logging.info("PySimConnect: Closing Socket")
        
class SimConnect(object):
    
    def Load_Flightplan(self, fileloc):
        #Request Data on SimObject 0xe
        #d = self.string256(fileloc)
        d = fileloc.ljust(260, chr(0))
        self.client.send(d, 0x3f)
    
    def create_DataDefinition(self, id):
        t = DataDefinition(self,id)
        self.data_dict[id] = t
        return t
        
    def create_EventList(self):
                e = EventList(self)
                return e    
    
    def string256(self, s): #Takes a string and returns it padded to 256
        return s.ljust(256, chr(0))
    
    def connected(self):
        #If go is true then connected
        return self.client.go
    
    
    def __init__(self, name, FSX_version, recieve):
        #Initalizes SimConnect
        #Depending on your FSX_version you are connecting to, need to set protocol etc.
#        self.read_buffer = ''
        self.data_dict = {}
        logging.debug("PySimConnect: FSX verison %d", FSX_version)
        if FSX_version == config.FSXSP0:
            FSX_subversion = 60905
            FSX_major_version = 10
            FSX_minor_version = 0
            FSX_name = "FSX"
            protocol = 2
        elif FSX_version == config.FSXSP1:
            FSX_subversion = 61355
            FSX_major_version = 10
            FSX_minor_version = 0
            FSX_name = "FSX"
            protocol = 3
        elif FSX_version == config.FSXSP2:
            FSX_subversion = 61259
            FSX_major_version = 10
            FSX_minor_version = 0
            FSX_name = "FSX"
            protocol = 4
        elif FSX_version == config.ESP :
            FSX_subversion = 20
            FSX_major_version = 1
            FSX_minor_version = 0
            FSX_name = "ESP"
            protocol = 4
            
        #self.app_name = name
        self.client = SimConnect_Client_c(name, protocol, FSX_name, FSX_major_version, FSX_minor_version, FSX_subversion, recieve)
        self.data_list = [] #Sets up data list will be object eventually

    def connect(self, addr, port, connect):
        self.client.daemon = False
        comm = self.client.connect(addr,port)
        if (connect & comm): self.client.start()
        return comm
    
    def close(self):
        #Closes the connection with FSX
        self.client.close()
    
    def quit(self):
        self.client.quit()
        
    def receive(self):
    
    
        def decode_packet(packet_data):
            packet_type = packet_data[0]
            data = packet_data[1]
            #print packet_type, data
            if packet_type == 8: #Receive data on SimObject
                #print "%r" %data
                #Get 1st 7 ints
                out = struct.unpack('<7I', data[:28])
                request_id = out[0]
                id = out[2]
                #print out
                #Get the correct data_definition
                data_def = self.data_dict[id]
                parsed = struct.unpack(data_def.unpack_s, data[28:])
                #Set values
                i =0
                #print parsed
                for v in parsed:
                    if not data_def.objlist[i].inhibit:
                        if data_def.list[i].func == None:
                            data_def.objlist[i].value = v
                        else:
                            data_def.objlist[i].value = data_def.list[i].func(v)
                    else: #If not inhibit
                        data_def.objlist[i].inhibit -= 1
                    #print data_def.objlist[i], v
                    i+=1
                return id
            else:
                logging.warning("PySimConnect Decode Packet: Error Type Equals %r", packet_type)
                return -1
            
            
        status = False    #Check packet data to see if any data is in there.
        define_id = [] #Empty list
        while len(self.client.packet_data) > 0:
           # print "Decoding Packet", len(self.client.packet_data)
           # print "%r" %self.client.packet_data
            status = True
            define_id.append(decode_packet(self.client.packet_data.pop(0)))

        return define_id
    
if __name__ == '__main__':
    s = SimConnect('RJGlass_As', 2, True)
    s.connect('192.168.1.37', 1500, True)
    s.receive()
    s.Load_Flightplan('DTWCVG')
    #s.definition_0 = s.create_DataDefinition(7)
    #airspeed = data_obj(0.00)
    #s.definition_0.add("Airspeed Indicated", "knots", FLOAT32, airspeed)
    #print airspeed.value
    #s.receive()
    #alt = data_obj(200.0)
    #s.definition_0.add("Indicated Altitude", "feet", FLOAT32, alt)
    #AGL = alt.get
    #s.receive()
    #s.definition_0.request(4, DataDefinition.USER, DataDefinition.VISUAL_FRAME, interval = 10)
    #while True:
    time.sleep(13)
    s.close()