#VSI
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
    #VSI
     
    
    def __init__(self, *args, **kwds):
        
        super(gauge_c, self).__init__(*args, **kwds)
        
        self.x = 90
        self.y = 175
        self.set_native_size(self.x, self.y)
        
               
        
        
        #Init Constants
        self.radius = 70
        #Init Variables
        self.a = 0
        self.dt_count = 0
        #Init Sim Variables
        self.vs = variable.variables.load(0x115,'4F')
        
        
        self.load_batch()
      
        
        
    def comp(self, dt):
            pass
            
            
            
            
            
    def load_batch(self):
        self.marks_shape = self.marks_b()
        self.pointer_shape = self.pointer_b()
        
        
    def pointer_b(self):
        
        v1 = common.vertex.lines()
        v2 = common.vertex.lines()
        r = [-62,-35,-25] 
        w = 5
        w2 = 1
        
        v1.add([r[0],0,r[1],w,r[1],-w,r[0],0])
        v1.reset()
        v1.add([r[1],0,r[2],0])
        v2.add([r[0],0,r[1],w,r[1],-w,r[0],0])
        
        batch = pyglet.graphics.Batch()
        b1 = batch.add(v1.num_points, GL_LINES, None, ('v2f', v1.points),('c3f',common.color.green*v1.num_points))
        b2 = batch.add(v2.num_points, GL_POLYGON, None, ('v2f', v2.points),('c3f',common.color.green*v2.num_points))
            
        return batch
        #glBegin(GL_LINES)
        #        glVertex2f(40.0, 0.0)
        #        glVertex2f(0.0, 0.0)
        #        glEnd()
        #        glBegin(GL_POLYGON)
         #3       glVertex2f(0.0, 0.0)
        #        glVertex2f(30.0, 5.0)
        #        glVertex2f(30.0, -5.0)
        #        glEnd()
        
    def marks_b(self):
                
                def rot(xy, angle):
                    rad = math.radians(-angle)
                    s = math.sin(rad)
                    c = math.cos(rad)
                    return [xy[0]*c-xy[1]*s, xy[0]*s+xy[1]*c]
                
                def text(x,y, s):
                    glPushMatrix()
                    glTranslatef(x,y-6.0,0.0)
                    glScalef(0.13, 0.13, 0.0)
                    glText(s)
                    glPopMatrix()
                    
                large = 15
                med = 10
                small = 5
                radius = self.radius
                
                    
                v1 = common.vertex.lines()
                #Set up lists with degree marks 
                a = [large] *3 + [small] * 4 + [med] + [small] * 4
                size = a + [large] + a[::-1] #Above + large at 0 + reverse of above
                #Now Degrees to rotate
                rotations = [15] * 2 + [6] * 20 + [15] *3
                angle = 180
                #glColor(white)
                #glLineWidth(2.0)
                #glPushMatrix()
                #Go through all point on list
                for i in range(25):
                    
                    v1.add(rot([0,radius], angle))
                    v1.add(rot([0,radius-size[i]], angle))
                    v1.reset()
                    angle+=rotations[i]
                    #glRotate(rot[i], 0.0, 0.0, 1.0)
                #glPopMatrix()
                batch = pyglet.graphics.Batch()
                b1 = batch.add(v1.num_points, GL_LINES, None, ('v2f', v1.points),('c3f',common.color.white*v1.num_points))
            
                return batch
   
    def draw_nums(self):
        
        def text_xy(x,y,s):
            glPushMatrix()
            glTranslatef(x+5,y,0)
            glScalef(0.13,0.14,1.0)
            text.write(s)
            glPopMatrix()
    #Draw text 1,2,4 on top and bottom and appropriate spot
        x1, y1 = -46.0, 70
        x2, y2 = -26.0, 78
        x4, y4 = -4.0, 82
        # 1's
        text_xy(x1,y1, "1")
        text_xy(x1, -y1, "1")
        #2's
        text_xy(x2,y2, "2")
        text_xy(x2, -y2, "2")
        #4's
        text_xy(x4,y4, "4")
        text_xy(x4, -y4, "4")
        
    def draw_value(self, vs):
        #Draw text in center of guage
       
        glPushMatrix()
        glTranslatef(-18.0, 0.0, 0.0)
        glScalef(0.13, 0.15, 0.0)
        value = round(abs(vs / 1000.0), 1)
        if value >=10:
            text.write("%2.0f" %value, 100)
        else:
            text.write("%2.1f" %value, 100)
        glPopMatrix()
        
    def draw_pointer(self, vs):
        #Draw Pointer, convert vertical speed to correct angle
        value = abs(vs) #Disregard negative for now.
        #Determine appropriate angle
        if value <=1000: #Linear up to 1000
        #1000 foot mark is at angle 60 degrees
            angle = value / 1000.0 * -60 #make float
        else: #Value above 1000' exp scale
            if value >4500: value=4500 #Put upper limit on guage
            x = (value / 1000.0) - 1.0
            y = (-1.0/6*x*x)+(7.0/6*x)
            #print y
            #y=1 at 2000 foot mark 15deg, y =2 at 4000 ft mark 30deg
            angle = -60 - (y * 15)
        if vs <=0: angle = angle * -1.0 #If VS negative then make angle -
        glRotatef(angle,0,0,1)
        self.pointer_shape.draw()
        
         
    def draw(self):
        vs = int(self.vs.value)
        #self.comp(self.dt)
        glLineWidth(2.0)
        common.color.set(common.color.white)
        glPushMatrix()
        glTranslatef(35,0,0)
        self.marks_shape.draw()
        self.draw_nums()
        common.color.set(common.color.green)
        self.draw_value(vs)
        self.draw_pointer(vs)
        glPopMatrix()
      
