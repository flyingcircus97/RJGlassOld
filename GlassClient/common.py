#common.py
# -- Common function used by all guages
import math

class color_c(object):
    def __init__(self):
        self.white = (1.0,1.0,1.0)
        self.yellow  = (1.0,1.0,0.0)
    

class xycalc_c(object):
    
    def rotate(self, x,y, deg):
        rad = math.radians(deg)
        x1 = x * math.cos(rad) - y * math.sin(rad)
        y1 = x * math.sin(rad) + y * math.cos(rad)
        return [x1,y1]
        
        
class vertex(object):
    
    class lines(object):
        #Used to take points of a line_strip and convert to lines for batch processing

        def __init__(self):
            self.points = [] #list convert to points for lines
            self.list = [] #Line strip
            self.count = 0
        
        def add(self, list):
            while len(list)>=2:
                pop = list[:2]
                list = list[2:]
                if self.count > 1:
                    self.points.extend(self.points[-2:]) #Tack on last point if not new point
                self.points.extend(pop)
                self.count += 1
                self.list.extend(pop) #Standard list
                
        def reset(self):
            #Restarts line_strip for lines calc
            self.count =0
            
            
xycalc = xycalc_c()    
color = color_c()    
    
#vertex = vertex_c()
#a = vertex_c.list_c()