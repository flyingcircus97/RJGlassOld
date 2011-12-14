#!/usr/bin/env python
import variables.variable as variable
import config
import FlightSim.comm
from GlassController import controller, connections
import time
try:
    import json
except ImportError:
    import simplejson as json 

#print controller
#Create AJAX Func Dict
class AJAX_c(object):
    
    def __init__(self):
        self.create_func_dict()
        self.variables = variable.variables
        self.connection = config.connection
    def create_func_dict(self):
        self.func_dict = {}
        self.func_dict['var_tree'] = self.var_tree
        self.func_dict['get_var'] = self.get_var
        self.func_dict['var_values'] = self.get_var_values
        self.func_dict['set_var'] = self.set_var_value
        self.func_dict['comm_status'] = self.comm_status
        self.func_dict['comm_update'] = self.comm_update
        self.func_dict['connection'] = self.connection
        self.func_dict['server'] = self.server
        self.func_dict['conn_log'] = self.conn_log
        self.func_dict['script'] = self.scripts
        
    def process_AJAX(self, method, body):
        out = None
        if method in self.func_dict:
            out = self.func_dict[method](body)
            
        return out
    
    def get_key(self, body, key):
        #Looks for key/argument in body of request
        if body == None:
            return None
        else:
            if key not in body.keys():
                return None
            else:
                return body[key]
            
    
    def var_tree(self, body):
    
        def get_children(var_group, name):
            children = []
            #Sort children alphabetically
            for i in sorted(var_group.keys()):
                if name == None:
                    full_name = i
                else:
                    full_name = name + '.'+ i #Used to get full path to var, for future AJAX request.
                d={}
                d["property"] = {"name":i, "key": full_name}
                
                if type(var_group[i]) == dict: 
                    d["children"] = get_children(var_group[i], full_name)
                children.append(d)
            return children	
        #Create Tree Directory, JSON.
        var_groups = self.variables.var_groups
        #print "*******"
        var_d = {}
        var_d["property"] = {"name": "All", "key" : "All"}
        var_d["children"] = get_children(var_groups, None)
        #print var_d
        #m = json.dumps([{"property": {"name": "root"}}])
        m = json.dumps([var_d])
        #print variable.variables.var_groups
        #print m
        return m
        
    def get_var(self,body):
            list = []
            #print body
            #print json.loads(body)
            keys = body['var'][0].split(',')
            for key in keys:
                for i in self.variables.get_varAJAX(key):
                    list.append(i)
                
            #Check to see if list is empty, if so, put Empty table up.
            if len(list) == 0:
                list = [['  No Variable Groups Selected']]
            return  json.dumps(list)
        
    def get_var_values(self,body):
            list = []
            #print body
            #print json.loads(body)
            keys = body['var'][0].split(',')
            for key in keys:
                for i in self.variables.get_varAJAX(key, values_only = True):
                    if len(i) > 1:
                        list.append(i[1])
                    else:
                        list.append('None')
                
            #print list
            return  json.dumps(list)   
        
    def set_var_value(self, body):
        #Called to set variable from Website.
            
            addr = int(body['addr'][0],16)
            r = self.variables.set_string(addr,body['value'][0])
            
            
            return json.dumps([r,self.variables.get_string(addr)])
            
    def comm_status(self, body):
            #FlightSim.comm.FS_Comm.disconnect()
            comm = FlightSim.comm.FS_Comm
          
            
            return json.dumps([comm.sim_name,comm.status_message])
            
    def comm_update(self, body):
        
          #Check for status, disconnect or connect if applicable.
        comm = FlightSim.comm.FS_Comm
        status = self.get_key(body, 'status')
        if status !=None:
            status = status[0].lower()
            if status == 'disconnect':
                   
                comm.disconnect()
            elif status == 'connect':
                comm.connect()

            return "ok"
            
            
        
    def connection(self, body):
            action = body['action'][0]
            if action == 'save':
                #Save data
                i = int(body['index'][0])
                self.connection.save(i,body['name'][0],body['mode'][0],body['IP'][0], body['port'][0])
                active, data = self.connection.connection_data()
                out = json.dumps((i,data))
            elif action == 'new':
                selected = self.connection.new()
                active, data = self.connection.connection_data()
                out = json.dumps((selected, data)) 
                #Replaced active with selected.. So new selected configuration is selected.
            #print body
            elif action == 'delete':
                i = int(body['index'][0])
                selected = self.connection.delete(i)
                active, data = self.connection.connection_data()
                out = json.dumps((selected, data)) 
            elif action == 'connect':
                i = int(body['index'][0])
                #Save just incase any changed made.
                self.connection.save(i,body['name'][0],body['mode'][0],body['IP'][0], body['port'][0])
                comm = FlightSim.comm.FS_Comm
                comm.disconnect()
                time.sleep(2)
                self.connection.set_active(i)
                comm.setup_sim(self.connection.active)
                out = 'ok_connect'
            else:
                out = json.dumps(self.connection.connection_data())
            return out
    def server(self, body):
        j = {}
        j['connections'] = connections.AJAX_list()
        j['port'] = controller.Glass_Server.port
        out = json.dumps(j)
        return out
    
    def conn_log(self,body):
        i = int(body['index'][0])
        out = json.dumps(connections.AJAX_log(i))
        return out
    
    def scripts(self,body):
        l = body['active'][0]
        if l!="":
            l = json.loads(l)
        else:
            l = None
        out = json.dumps(controller.gstest.AJAX_list(l))
        return out
        
AJAX = AJAX_c()
def process_AJAX(method, body):
    return AJAX.process_AJAX(method, body)
    
    
