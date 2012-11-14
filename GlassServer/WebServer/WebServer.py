#!/usr/bin/env python
import string
import urllib
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import ThreadingMixIn
import cgi, time
import threading
import variables.variable as variable
import FlightSim.comm
import AJAX
try:
    import json
except ImportError:
    import simplejson as json 


class GlassHandler(SimpleHTTPRequestHandler):
    
   
    #This overides logging of requests to screen
    def log_message(self, format, *args): 
        pass
    
    def do_GET(self):
        #self.timeout = 5.0
        #self.connection.settimeout(5.0)
        #print 'Get', self.client_address
        path_split = self.path.split('/')
        #print path_split
        if path_split[1] == 'ajax':
            return self.do_AJAX(path_split[2])
        else:
            return SimpleHTTPRequestHandler.do_GET(self)
    
    def do_AJAX(self, qs):
        #self.timeout = 5.0
        #self.connection.settimeout(5.0)
        #print 'GET', self.path, self.client_address
        qspos = qs.find('?')
        if qspos>=0:
            body = cgi.parse_qs(qs[qspos+1:], keep_blank_values=1)
            method = qs[:qspos]
#            self.path = self.path[:qspos]
            #print body
            #if 'disconnect' in body.keys():
            #    print "DISCONNECT"
            #    FlightSim.comm.FS_Comm.disconnect()
            #elif 'connect' in body.keys():
            #    print "CONNECT"
            #    FlightSim.comm.FS_Comm.connect()
        else:
          method = qs
          body = None
          
        # length = int(request.headers.getheader('content-length'))        
       # data_string = request.rfile.read(length)
       # print 'Data' , data_string, length
        
        out = AJAX.process_AJAX(method, body)
        IAS = "%5.1f" %variable.variables.byName("IAS").data.value
        #out = json.dumps({'age':{'test' :IAS}})
        #Return Data
        if out != None:
          self.send_response(200)
          self.send_header('Content-type', 'text/html')
          self.send_header('Content-Length', str(len(out)))
       #   self.send_header('Connection', 'Keep-Alive')
       #   self.send_header('Keep-Alive', 'timeout =5, max=97')
          self.send_header('Transfer-Encoding', 'chunked')
          self.end_headers()
          self.wfile.write(out)
        else: #No Data sent back, no ajax function found.
          self.send_response(400)
        
        #time.sleep(2)
        #self.wfile.write(out)
        
        return
        
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

        
class GlassWebServer_c(object):

    def serve_forever(self):
        self.webserver.timeout = 3.0
        while self.go:
            self.webserver.handle_request()
    
    def __init__(self, port):
        
        self.go=True
        self.port = port
       #self.webserver = HTTPServer(('', 8080), GlassHandler)
        self.webserver = ThreadedHTTPServer(('', port), GlassHandler)
        self.webserver.daemon_threads = True
        self.server_thread = threading.Thread(target=self.serve_forever)
        self.server_thread.setDaemon(True)
        self.server_thread.start()
        
       
       #self.webserver.serve_forever()
       # except KeyboardInterrupt:
       #     print "Shutting Down"
       #     self.webserver.socket.close()
        print "GlassWebServer running in thread:", self.server_thread.getName()
           
    def quit(self):
        print "Quitting WebServer"
        self.go=False
        #self.webserver.shutdown()
        #time.sleep(1.0)
        
        #urllib.urlopen("http://localhost:8080/WebServer")
        #print "GlassWebServer is Running: ", self.server_thread.isAlive()
        #print "Quitting WebServer Done"
        
