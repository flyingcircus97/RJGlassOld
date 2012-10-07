import pyglet
from pyglet.gl import *
from gauge import gauge_parent
import math

class gauge_c(gauge_parent):
    
    def __init__(self, *args, **kwds):
        
        super(gauge_c, self).__init__(*args, **kwds)
        
        self.x = 500
        self.y = 500
        self.set_native_size(self.x, self.y)
        self.earth = (0.69, 0.4, 0.0) #The ground color on attitude indicator
        self.sky = (0.0, 0.6, 0.8) 
        #For testing purposes
        self.a = 0.0
        self.pitch = 0
        pyglet.clock.schedule_interval(self.fade_in, .01) 
        
    
    def fade_in(self, dt):
        self.a+=.2
        if self.a>180.0:
            self.a=-180.0
        #if self.a == -3.0:
        #    self.pitch +=2
        
    def draw(self):
        slope = self.draw_horizon(self.a,self.pitch)
        self.pitch_marks(self.a, self.pitch, 2, 5)
        self.draw_border()
        
            
    def pitch_marks(self, roll, pitch, line_width, pixel_per_degree):
            def get_width(pitch):
                x = int(round(pitch / 2.5))
                if x==0:
                    w = 0 #Horizon is draw during in draw_horizon()
                elif (x % 4) == 0:
                    w = 30
                elif (x % 2) ==0:
                    w = 15
                else:
                    w = 5
                return w
            glPushMatrix()
            #Rotate with roll
            glRotatef(roll,0,0,1)
            
            
            #Draw the pitch marks
            #Uses pitch to determine which pitch lines need to be drawn
            #pixel_per_degree = 7.25 Starts 12.5 degrees down and goes up 11 lines
            start_point = 12.5
            num_lines = 11
            glColor3f(1.0,1.0,1.0)
            
            glLineWidth(line_width)
            #pitch = pitch * -1
            #Round pitch to nearest 2.5 degrees
            start = round(pitch / 2.5) * 2.5
            start = start - start_point # Go down 25 degrees
            y = start* pixel_per_degree
            #glTranslatef(0.0, start * pixel_per_degree, 0.0)
            point_l = []
            for i in range(num_lines):
                w = get_width(start)
                if w>0:
                    #glBegin(GL_LINES)
                    #glVertex2f(-w, 0.0)
                    #glVertex2f(w, 0.0)
                    #glEnd()
                    point_l.extend([-w,y,w,y])
                #if (w==30): #Draw number for degrees
                #    c = int(round(abs(start))) / 10 + 48
                #    if (c>48): #If greater than 0
                #        glPushMatrix()
                #        glTranslatef(30.0, -6.0, 0.0) #Move over to right (Numbers only on right side)
                #        glPushMatrix()
                #        glScalef(0.13, 0.13, 1.0) #Scale down for numbers
                #        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)
                #        glutStrokeCharacter(GLUT_STROKE_ROMAN, 48)
                #        glPopMatrix()
                #        glPopMatrix()
                y+=2.5 * pixel_per_degree
                #glTranslatef(0.0, 2.5 * pixel_per_degree, 0.0)
                start = start + 2.5
            pyglet.graphics.draw(len(point_l)/2, pyglet.gl.GL_LINES,
                ('v2f', point_l ))    
            glPopMatrix()
    
    
    def draw_horizon(self, roll, pitch):
        
        def find_side(xy):
            #Determins the side of A.Horizon point resides on. 
            #Side 0=right, 1=bottom, 2=left, 3=top
            x = xy[0]
            y = y[0]
            
        y = int(-pitch * 500.0 / 20)
        slope = math.tan(math.radians(roll))
        w = 250
        h = 250
        corners = [[w,-h],[-w,-h],[-w,h],[w,h]]
        #Determine right and left points.
        #Right point
        rx2 = w
        ry2 = int(y + slope*w)
        r_side = 0
        if ry2 > h: #Goes above gauge
            ry2 = h
            r_side = 3
            #Need to determine x cordinate
            if slope ==0:
                rx2 = None
            else:
                rx2 = int(1.0*(h-y)/slope)
                
                #if math.fabs(rx2>w):
                #    rx2 = None
        elif ry2<-h: #Goes below gauge
            ry2 = -h
            r_side = 1
            if slope == 0:
                rx2 = None
            else:
                rx2 = int(1.0*(-h-y)/slope)
                
                #if math.fabs(rx2>w):
                #    rx2 = None
        #Left point
        lx2 = -w
        ly2 = int(y + slope*-w)
        l_side = 2
        if ly2 > h: #Goes above gauge
            ly2 = h
            l_side = 3
            #Need to determine x cordinate
            if slope ==0:
                lx2 = None
            else:
                lx2 = int(1.0*(h-y)/slope)
                
                #if math.fabs(lx2>w):
                #    lx2 = None
        elif ly2<-h: #Goes below gauge
            ly2 = -h
            l_side = 1
            if slope == 0:
                ly2 = None
            else:
                lx2 = int(1.0*(-h-y)/slope)
                
                #if math.fabs(lx2>w):
                #    lx2=None
        #ly2 = int(y - slope*250)
        #if ((rx2<>None) and (lx2<> None)):
        if -90<roll<90:    
            t_color = self.sky
            b_color = self.earth
        else:
            t_color = self.earth
            b_color = self.sky
        pyglet.gl.glColor3f(*t_color)
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
            ('v2i', (-w,-h,-w,h,w,h,w,-h)))
        if (r_side<> l_side):
            ps = [lx2,ly2,rx2,ry2]
            horz_ps = ps
            c_index = r_side
            while c_index <> l_side:
                ps.append(corners[c_index][0])
                ps.append(corners[c_index][1])
                c_index+=1
                if c_index>3:
                    c_index = 0
            ps.append(lx2)
            ps.append(ly2)
            #l_side = find_side((lx2,ly2))
            #r_side = find_side((rx2,ry2))
            #print ps
            pyglet.gl.glColor3f(*b_color)
            pyglet.graphics.draw(len(ps)/2, pyglet.gl.GL_POLYGON,
                ('v2i', ps))
            pyglet.gl.glColor3f(1,1,1)
            pyglet.graphics.draw(len(ps)/2, pyglet.gl.GL_LINES,
                ('v2i', horz_ps ))    
            
        return slope    
        #self.a+=0.01
        