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
import logging


def init_log():
    level = logging.INFO
    if '-debug' in sys.argv:
        level = logging.DEBUG
    logging.basicConfig(level=level, format='%(asctime)s.%(msecs)d %(levelname)s:%(message)s', datefmt='%H:%M:%S')
    #Set up File log
    logger = logging.getLogger()
    handler = logging.FileHandler('GlassServer.log', mode='w')
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s.%(msecs)d %(levelname)s:%(message)s', '%H:%M:%S'))
    logger.addHandler(handler)

class mainloop_c(object):
    
    def __init__(self):
        #Init Logging
        init_log()
        #Import Server/Client Modules
        from GlassController import controller
        from WebServer.WebServer import GlassWebServer_c
        from IOCP.IOCPClient import IOCPComm
        self.controller = controller
        self.webserver = GlassWebServer_c(config.general.webserver_port)
        self.IOCPclient = IOCPComm(config.general.IOCP_client)
        #Initalize variables
        self.go = True       
        self.loop_time= 1/60.0
        
#    def init_log(self):
#        print "Initialize Logging"
#        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)d %(levelname)s:%(message)s', datefmt='%H:%M:%S')
        
    def run(self):
        logging.info('MainLoop Started')
        
        try:
            while self.go:
                time.sleep(self.loop_time)
                self.controller.FS_Comm.process()
                self.controller.comp()
                self.controller.variables.change_check()
                
                
        except KeyboardInterrupt:
            logging.warning('Main Loop - Keyboard Interrupt')
            self.quit()
        #Shut down server
        
        
    def quit(self):
        self.go = False
        logging.info('Glass Server Quiting')
        #try:
        self.IOCPclient.quit()
        self.controller.quit()
        self.webserver.quit()
        time.sleep(3)
        logging.info("Threads Active - %r", threading._active)
        logging.shutdown()
        #sys.exit()
        #os._exit(os.EX_OK)
        os._exit(0)
        sys.exit()
        
        
mainloop = mainloop_c()

def run():
    mainloop.run()
    
def quit():
    mainloop.quit()
    

    
if __name__ == '__main__':
    
    print "Press Ctrl-C to Quit"
    
    run()
 
 