#variable.py Module
# -- Used to communicate with GlassServer on behalf of all guages.


class variables_c(object):
    #Class that holds on the variables for the guages
    
    def __init__(self):
        
        self.dict = {} #Dictionary holds variable objects by hex ID
        self.keys = []
        
        
    def load(self, hex, init_value = 0.0):
        #Gets varible is already exists.
        #Adds variable to variables dict if doesn't exist
        #Returns variables.
        
        if hex not in self.dict.keys():
            self.dict[hex] = variable_c(hex, init_value)
            
        self.keys = self.dict.keys()
        return self.dict[hex]
    
    def list(self): #Gets list of all variables
        return self.keys
    
    def exists(self, hex): #Check if variable exists
        return hex in self.keys
    
    
        
        
class variable_c(object):
    #Variable object.
    
    def __init__(self, hex, init_value = 0.0):
        self.hex = hex
        self.type = None
        self.value = init_value
        #Temp for tesing
        self.pack_size = 4
        self.format_s = '9.5f'
        self.pack_format = 'f'
    
    def setvalue(self, value):
        self.value = value

variables = variables_c()