"""
PI_UDPGlassServer.py

Creates a UDP server inside of X-Plane to communicate with RJGLass GlassServer...


"""

from XPLMProcessing import *
from XPLMDataAccess import *
from XPLMUtilities import *
from XPLMMenus import *
from XPLMPlanes import XPLMAcquirePlanes, XPLMCountAircraft, XPLMReleasePlanes, XPLMGetNthAircraftModel, XPLMSetAircraftModel, XPLMSetActiveAircraftCount
import socket #Used for UDP server.
import GlassData
import os, struct, time

class PythonInterface:
    def create_socket(self):
    #Create UDP Server
        self.UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = ('', 21567) #Accept data from any IP on said port.
        self.UDPSock.bind(self.addr)
        self.UDPSock.setblocking(0)
        self.UDPTimeout = XPLMGetElapsedTime() #Set Timeout to sim time
        
    def reset_socket(self):
        self.UDPSock.close()
        self.create_socket()
        print "RESETING SOCKET ****"
        
    def XPluginStart(self):
        #global gOutputFile, gPlaneLat, gPlaneLon, gPlaneEl
        self.Name = "UDPGlassServerComm"
        self.Sig =  ""
        self.Desc = "UDP connection for Glass Server to communicate with XPlane 10"
        self.ready = False
#		self.CP_set = False
        
        
        """
        Register our callback for once second.  Positive intervals
        are in seconds, negative are the negative of sim frames.  Zero
        registers but does not schedule a callback for time.
        """
        self.FlightLoopCB = self.FlightLoopCallback
        XPLMRegisterFlightLoopCallback(self, self.FlightLoopCB, 1.0, 0)
        
        return self.Name, self.Sig, self.Desc
        
    def PostPlaneLoaded(self):
        #Loop here until one of Greg's F16 dataref are found, (i.e. wait for plane to load)
        #time.sleep(2)
        
        
        """ Find the data refs we want to record."""
        self.data_out_list = GlassData.data_list(1)
        self.data_in_list = GlassData.data_list(1)
        #self.data_out_list.add("sim/flightmodel/position/latitude",'f')
        #self.data_out_list.add("sim/flightmodel/position/longitude", 'f')
        #self.data_out_list.add("sim/flightmodel/position/indicated_airspeed", 'f')
#		self.data_out_list.add("sim/flightmodel/position/magpsi", 'f')
        self.data_out_list.add("sim/flightmodel/position/phi", 'f', lambda x:-x)   #Roll
        self.data_out_list.add("sim/flightmodel/position/theta", 'f') #Pitch
        
#		self.data_out_list.add("sim/flightmodel/position/vh_ind_fpm", 'f')
#		self.data_out_list.add("sim/flightmodel/position/elevation", 'f', lambda x:x*3.2808)
#		self.data_out_list.add("sim/flightmodel/misc/machno", 'f')
#		self.data_out_list.add("sim/aircraft/view/acf_Vne", 'f')
#		self.data_out_list.add("sim/flightmodel/position/alpha", 'f')
#		self.data_out_list.add("sim/flightmodel/position/magnetic_variation", 'f')
        #Engine
#		self.data_out_list.add("sim/flightmodel/engine/ENGN_oil_press_psi", 'f', lambda x:x*144, offset = 0)
#		self.data_out_list.add("sim/flightmodel/engine/ENGN_ITT_c", 'f', offset = 0)
#		self.data_out_list.add("sim/flightmodel/engine/ENGN_N2_", 'f', offset = 0)
        #self.data_out_list.add("sim/flightmodel/engine/ENGN_N1_", 'f', offset = 0)
        #self.data_out_list.add("sim/flightmodel/engine/ENGN_FF_", 'f', lambda x:x*7936.64, offset = 0) #convert KG/s to PPH
        #Gear and Speed Brakes Handles
#		self.data_out_list.add("sim/cockpit/switches/gear_handle_status", 'i')
        #self.data_out_list.add("sim/flightmodel/controls/sbrkrqst", 'f')
#		self.data_out_list.add("sim/flightmodel2/controls/speedbrake_ratio", 'f')
#		self.data_out_list.add("sim/flightmodel/position/latitude", 'f', lambda x:x*3.141/180)
#		self.data_out_list.add("sim/flightmodel/position/longitude", 'f', lambda x:x*3.141/180)
                
        #
        #self.data_in_list.add_in("sim/cockpit/switches/gear_handle_status", 'i', 'TOGGLE', lambda x:1-x)
#		self.data_in_list.add_in("sim/cockpit/switches/gear_handle_status", 'i', 'BUTTON', lambda x:5)  #lambda function always returns button number
        #reset_command = XPLMCreateCommand("sim/operation/reset_flight","Reset Flight")	
#		self.data_in_list.add_in("sim reset button", 'i', 'COMMAND', lambda x:"sim/operation/reset_flight")
#		self.data_in_list.add_in("sim rec button", 'i', 'COMMAND', lambda x:"sim/operation/quicktime_record_toggle")
#		self.data_in_list.add("sim/time/sim_speed", 'i')
        
        
        #Create UDP Server
        self.create_socket()
        #self.UDPSock.sendto("STARTING", self.addr)
        
        self.ready = True #Ready to go
        
                
        

            
    def XPluginStop(self):
        # Unregister the callback
        XPLMUnregisterFlightLoopCallback(self, self.FlightLoopCB, 0)

        # Close the file
        #self.OutputFile.close()


    def XPluginEnable(self):
        return 1

    def XPluginDisable(self):
        pass

    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
        pass

    def PlanesAvailableCallback(self):
        print "GO"

    def FlightLoopCallback(self, elapsedMe, elapsedSim, counter, refcon):

        if self.ready:
             #Ready to go
            # The actual callback.  First we read the sim's time and the data.
            self.elapsed = XPLMGetElapsedTime()
            if (self.elapsed - self.UDPTimeout)>= 10:
                self.reset_socket()
                    #self.test()
                #if int(self.elapsed) == 5:
                #		self.test()
                #print self.elapsed	
            
            
            self.data_out = self.data_out_list.make_data_string()
            #print self.data_out
            temp = len(self.data_out)
            #self.data_out += MultiAircraft.data_out_s(self.MP)
            #self.data_out += self.waypoint.next_point() #struct.pack('ii10sfff', 0,0,'KLAX', 100, 34.5, -118.4)
            
            #Add aircraft data.
            #print temp, len(self.data_out) - temp
            print len(self.data_out)
            #print '%r' %(self.data_out)
            self.recv_data()
        
            # Return 1.0 to indicate that we want to be called again in 1 frame.
            return -1.0
        else:
            self.PostPlaneLoaded()
            return 1.0

    def recv_data(self):
        ok = False
        try:
            data_in, client_addr = self.UDPSock.recvfrom(1024)
            self.UDPTimeout = self.elapsed
            print "%r" %(data_in), client_addr
            if self.data_in_list.parse_data_in(data_in):
                    ok = True
            self.UDPSock.sendto(self.data_out, client_addr)
        except socket.error: #Error due to non blocking not receving anything.
            pass
        return ok
