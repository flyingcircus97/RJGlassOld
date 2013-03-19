#common.py
# -- Common function used by all guages
# Colors, Drawing func, 
import math
from pyglet.gl import glColor3f

class color_c(object):
    def __init__(self):
        self.white = (1.0,1.0,1.0)
        self.yellow  = (1.0,1.0,0.0)
        self.black = (0.0,0.0,0.0)
        self.purple = (1.0,0.0,1.0)
        self.cyan = (0.0,1.0,1.0)
        self.green = (0.0,1.0,0.0)
        self.red = (1.0,0.0,0.0)
    
    def set(self, c):
        glColor3f(c[0],c[1],c[2])

class xycalc_c(object):
    
    def rotate(self, x,y, deg):
        rad = math.radians(deg)
        x1 = x * math.cos(rad) - y * math.sin(rad)
        y1 = x * math.sin(rad) + y * math.cos(rad)
        return [x1,y1]

#Common drawing functions.
class draw_c(object): 

    def List_Circle(self, radius, segments, start_angle = 0, stop_angle = 360, start_tick = False, stop_tick = False, tick_radius = 0, offset_x = 0, offset_y = 0):
        #Returns list of points to make circle of given radius and angles
        step = (stop_angle - start_angle) / 1.0 / segments # /1.0 make sure returns float
        Deg_2_Rad = 3.14159265 / 180
        l = [] #Clear List
        angle = start_angle
        for i in range(segments+1):         
            rad = angle * Deg_2_Rad #Convert to radians
            x = radius * math.sin(rad)
            y = radius * math.cos(rad)
            if ((i == 0) & (start_tick == True)):
                x1 = tick_radius * math.sin(rad)
                y1 = tick_radius * math.cos(rad)
                l.extend([x1+offset_x,y1+offset_y])
            l.extend([x+offset_x,y+offset_y])
            if ((i == segments) & (stop_tick == True)):
                x1 = tick_radius * math.sin(rad)
                y1 = tick_radius * math.cos(rad)
                l.extend([x1+offset_x,y1+offset_y])
            angle+=step
        #After done whole circle return list    
        
        return l    
        
        
class vertex(object):
    
    class lines(object):
        #Used to take points of a line_strip and convert to lines for batch processing

        def __init__(self):
            self.points = [] #list convert to points for lines
            self.list = [] #Line strip
            self.count = 0
        
        def __len__(self):
            return len(self.points)
        
        def add(self, list):
            while len(list)>=2:
                pop = list[:2]
                list = list[2:]
                if self.count > 1:
                    self.points.extend(self.points[-2:]) #Tack on last point if not new point
                self.points.extend(pop)
                self.count += 1
                self.list.extend(pop) #Standard list
                self.num_points = len(self.points) // 2
                
        def reset(self):
            #Restarts line_strip for lines calc
            self.count =0
            
            
xycalc = xycalc_c()    
color = color_c()    
draw = draw_c()    
#vertex = vertex_c()
#a = vertex_c.list_c()