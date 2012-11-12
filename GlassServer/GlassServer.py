#!/usr/bin/env python
# ----------------------------------------------------------
# Glass Server
# ----------------------------------------------------------
# 
#
# use nc localhost 5004 in linux to test

# ---------------------------------------------------------------

import time
import sys, os
try:
    import config
except ImportError:
    print "PY2EXE"
    # We're in a py2exe, so we'll append an element to the (one element) 
    # sys.path which points to Library.zip, to the directory that contains 
    # Library.zip, allowing us to import config.py
    # Adds one level up from the Library.zip directory to the path, so import will go forward
    sys.path.append(os.path.split(sys.path[0])[0])
    import config
#from socket import *
import socket, select
import pickle
import string
import threading
from GlassController import controller
#import FMS_control
#import aircraft
#Constants
from WebServer.WebServer import GlassWebServer_c

class mainloop_c(object):
    
    def __init__(self):
        self.go = True       
        self.loop_time= 0.03
        self.controller = controller
        self.webserver = GlassWebServer_c(config.general.webserver_port)
    def run(self):
        #self.webserver = GlassWebServer_c()
        try:
            while self.go:
                time.sleep(self.loop_time)
                self.controller.FS_Comm.process()
                self.controller.comp()
                self.controller.variables.change_check()
                
        except KeyboardInterrupt:
            print "KEY INT"
        #Shut down server
        
        
    def quit(self):
        self.go = False
        print "QUITTING"
        #try:
        self.controller.quit()
        self.webserver.quit()
        time.sleep(3)
        print threading._active
        #sys.exit()
        os._exit(os.EX_OK)
        sys.exit()
        #except NameError:
        #    print "No Controller Exists to Kill"
    #def restart(self):
    #    self.quit()
    #    time.sleep(3)
    #    controller.init_server()
    #    time.sleep(3)
    #    self.run()
        
mainloop = mainloop_c()

def run():
    mainloop.run()
def quit():
    mainloop.quit()
    
if __name__ == '__main__':
    
    print "Press Ctrl-C to Quit"
    
    run()
        
        
    #import variable, aircraft, event
#    import variable
#    import modules
    #aircraft_data = aircraft.data()
#    variables = variable.variable_c()
#    variables.parse_variable_files(modules.variable_files)
#    print modules.variable_files
    #print modules.list #list of modules to go through
#    mod_data = mod_data_c(modules.mod_list, variables)
#    mike = variables.byName('IAS').data
    #events = event.event_c(aircraft_data)
#    glass = Glass_Server_c(variables)
#    print "SERVER is RUNNING"
#    for i in range(10):
#        time.sleep(2)
#        mod_data.test() #Here loop through all modules calling test method.
#        print mike.value
    #input("enter to quit")
#    print variables.dict
