#HSI
#-- Part of PFD
#

import pyglet
from pyglet.gl import *
from gauge import gauge_parent
import common
import variable
import math, time
import text



        
class gauge_c(gauge_parent):
    #HSI
     
    
    def __init__(self, *args, **kwds):
        
        super(gauge_c, self).__init__(*args, **kwds)
        
        self.x = 500
        self.y = 312
        self.set_native_size(self.x, self.y)
        
               
        self.load_batch()
        
        #Init Constants
        
        #Init Variables
        self.a = 0
        
      
        
        
    def comp(self):
            self.time = time.time()
            
            
            
            
    def load_batch(self):
        self.plane_shape = self.plane_figure_b()
        self.ticks_shape = self.ticks_b()
        self.triangle_marks = self.marks_b()
        
    def marks_b(self):
        
            def triangle_l(radius, w, h, angle):
                def rot(xy, angle):
                    rad = math.radians(-angle)
                    s = math.sin(rad)
                    c = math.cos(rad)
                    return [xy[0]*c-xy[1]*s, xy[0]*s+xy[1]*c]
                #Radius traingle is away from center, width, heigth, rotation angle
                #Returns list of points for batch
                l = []
                l.extend(rot([0,radius], angle))
                l.extend(rot([w,radius+h], angle))
                l.extend(rot([w,radius+h], angle))
                l.extend(rot([-w,radius+h], angle))
                l.extend(rot([-w,radius+h], angle))
                l.extend(rot([0,radius], angle))
                
                return l
            
            radius = 150
            
            
            v1 = common.vertex.lines()
            v1.add(triangle_l(radius - 2, 9, 15,0.0))
            v1.reset()
            v1.add(triangle_l(radius + 2, 5, 8, 45))
            v1.reset()
            v1.add(triangle_l(radius + 2, 5, 8, -45))
            v1.reset()
            v1.add([radius+5, 0, radius+20, 0]) #Right line
            v1.reset()
            v1.add([-(radius+5), 0, -(radius+20), 0]) #Left line
            
            batch = pyglet.graphics.Batch()
            b1 = batch.add(v1.num_points, GL_LINES, None, ('v2f', v1.points),('c3f',common.color.white*v1.num_points))
            
            return batch
            
    def plane_figure_b(self):
        
            
            v1 = common.vertex.lines()
            #Fuesalage
            v1.add([0,12,0,-35])
            v1.reset()
            #Wing (Note: Wing is located slightly below center (3pixels))
            v1.add([-25,-1,25,-1])
            v1.reset()
            #Tail
            v1.add([-13,-28,13,-28])
            
            batch = pyglet.graphics.Batch()
            b1 = batch.add(v1.num_points, GL_LINES, None, ('v2f', v1.points),('c3f',common.color.white*v1.num_points))
         
            return batch
        
    def ticks_b(self):
        
            radius = 145
            sm_tick = 15
            lg_tick = 20
            v1 = common.vertex.lines()
            deg = -150
            end_deg = deg*-1
            count = 0
            while deg <= end_deg:
                rad = math.radians(deg)
                sin = math.sin(rad)
                cos = math.cos(rad)
                v1.add([radius*sin, radius*cos])
                if count%2 == 0:
                    #Lg Tick
                    v1.add([(radius-lg_tick)*sin,(radius-lg_tick)*cos])
                else:
                    #Sm Tick
                    v1.add([(radius-sm_tick)*sin, (radius-sm_tick)*cos])
                v1.reset()
                deg +=5
                count +=1
            
            
            batch = pyglet.graphics.Batch()
            b1 = batch.add(v1.num_points, GL_LINES, None, ('v2f', v1.points),('c3f',common.color.white*v1.num_points))
         
            return batch
    
        
    def heading_ticks(self,radius, heading):
                
                def HSI_Text(i): #Returns text equivelent of tick mark
                    if i == 0:
                        return "N"
                    elif i== 9:
                        return "E"
                    elif i== 18:
                        return "S"
                    elif i== 27:
                        return "W"
                    else:
                        return str(i)
                    
                
                glPushMatrix()
                glRotatef(heading %10, 0.0, 0.0, 1.0)
                glLineWidth(2.0)
                common.color.set(common.color.white)
               
                self.ticks_shape.draw()
                #Draw Numbers / Letters
                #glRotatef(150,0,0,1) #Rotate -150 to start
                start = int(heading // 10)
                for i in range(0,36): #Draw tick ever 10 degrees
                    #Draw Number
                    if (start % 3) == 0: #Check to see if multiple of 3
                        glPushMatrix()
                        c = HSI_Text(start)
                        if len(c) == 2: #Two digits
                            glTranslatef(-6.0, 0.0, 0.0)
                        glTranslatef(-0.0, radius -30.0, 0.0)
                        glScalef(0.15, 0.15, 1.0)
                        text.write(HSI_Text(start))
                        glPopMatrix()
                    glRotatef(-10.0, 0.0, 0.0, 1.0) #Rotate 5 degrees
                    start = start + 1
                    if start == 36:start =0
                glPopMatrix()    
        
      
    def draw(self):
        
        self.comp()
        glLineWidth(2.0)
        #Move down
        glPushMatrix()
        glTranslatef(0,-30,0)
        self.plane_shape.draw()
        self.heading_ticks(145,self.a)
        self.triangle_marks.draw()
        glPopMatrix()
        #self.a+=1.0
        
        