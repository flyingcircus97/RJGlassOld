#Testing used, to manipulate.


class Test_c(object):
    
    def __init__(self, name):
        
        #self.variables = variables
        self.func_list = []
        self.func_list_count = 0
        self.active = True
        self.name = "Not Set"
        self.filename = name.split('.')[-1]+'.py'
        self.message = "--" #Used to put message on Scripts tab on webpage.
        
    def step(self):
        if self.active:
            if len(self.func_list) >0:
                func = self.func_list[self.func_list_count] #Run function
                func()
                self.func_list_count += 1
                if self.func_list_count >= len(self.func_list):
                    self.func_list_count = 0
                
            
    def add_func(self, func):
        self.func_list.append(func)             