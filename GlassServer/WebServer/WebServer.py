#!/usr/bin/env python
import string
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
    
    #def __init__(self, request, client_address, server):
    #    self.do_SHIT = copy(self.do_GET)
    #    SimpleHTTPRequestHandler.__init__(self, request, client_address, server)
    #def __init__(self, server_address, RequestHandlerClass, variables):
    #    SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)
        #self.aircraft = aircraft_data #This is so the handler can access the aircraft data.
    #    self.variables = variables

    #This overides logging of requests to screen
    #def log_message(self, format, *args): 
    #    pass
    
    def do_GET(self):
        #print 'Get', self.client_address
        path_split = self.path.split('/')
        #print path_split
        if path_split[1] == 'ajax':
            return self.do_AJAX(path_split[2])
        else:
            return SimpleHTTPRequestHandler.do_GET(self)
    
    def do_AJAX(self, qs):
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
          self.send_header('Connection', 'Keep-Alive')
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

    
    def __init__(self, port):
        self.port = port
       #self.webserver = HTTPServer(('', 8080), GlassHandler)
        self.webserver = ThreadedHTTPServer(('', port), GlassHandler)
        server_thread = threading.Thread(target=self.webserver.serve_forever)
        server_thread.setDaemon(True)
        server_thread.start()
       
       #self.webserver.serve_forever()
       # except KeyboardInterrupt:
       #     print "Shutting Down"
       #     self.webserver.socket.close()
        print "GlassWebServer running in thread:", server_thread.getName()
           
    def quit(self):
        self.webserver.shutdown()
        
