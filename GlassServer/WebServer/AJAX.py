#!/usr/bin/env python
import variables.variable as variable
try:
    import json
except ImportError:
    import simplejson as json 

#Create AJAX Func Dict
class AJAX_c(object):
    
    def __init__(self):
        self.create_func_dict()
        self.variables = variable.variables
        
    def create_func_dict(self):
        self.func_dict = {}
        self.func_dict['var_tree'] = self.var_tree
        self.func_dict['get_var'] = self.get_var
        self.func_dict['var_values'] = self.get_var_values
        self.func_dict['set_var'] = self.set_var_value
        
    def process_AJAX(self, method, body):
        out = None
        if method in self.func_dict:
            out = self.func_dict[method](body)
            
        return out
            
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
                for i in self.variables.get_varAJAX(key):
                    if len(i) > 2:
                        list.append(i[3])
                    else:
                        list.append('None')
                
            #print list
            return  json.dumps(list)   
        
    def set_var_value(self, body):
        #Called to set variable from Website.
            
            addr = int(body['addr'][0],16)
            r = self.variables.set_string(addr,body['value'][0])
            
            
            return json.dumps([r,self.variables.get_string(addr)])
            
            
    
AJAX = AJAX_c()
def process_AJAX(method, body):
    return AJAX.process_AJAX(method, body)
    
    
