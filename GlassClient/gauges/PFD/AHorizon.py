import pyglet
from pyglet.gl import *
from gauge import gauge_parent
import common
import variable
import math, time
import text


class gauge_c(gauge_parent):
    
    def __init__(self, *args, **kwds):
        
        super(gauge_c, self).__init__(*args, **kwds)
        
        self.x = 300
        self.y = 300
        self.set_native_size(self.x, self.y)
        
        self.earth = (0.69, 0.4, 0.0) #The ground color on attitude indicator
        self.sky = (0.0, 0.6, 0.8) 
        self.pixel_per_degree = 7.5
        
        self.load_batch()
        
        #Init Variables
        self.a = 0.0
        self.pitch = variable.variables.load(0x126,'4F')
        self.roll = variable.variables.load(0x125, '4F')
        
        #self.pitch = 8.5
        #pyglet.clock.schedule_interval(self.fade_in, .03) 
        #print self.pitch2.hex
        #pyglet.clock.schedule_interval(self.update, 1.0/30.0)
        #pyglet.clock.set_fps_limit(30.0)
        
        
    def load_batch(self):
        self.bV_shape = self.Center_Mark_V()
        self.static_triangle_shape = self.static_triangles()
        self.white_triangle, self.yellow_triangle = self.dynamic_triangle()
        self.white_slip, self.yellow_slip = self.slip_indicator()
        
    def dynamic_triangle(self):
            radius = 120.0
            size = 8.0
            
            triangle = common.vertex.lines()
            #Draw actually traingle
            triangle.add([0.0,radius])
            triangle.add([size, radius - size *2])
            triangle.add([-size, radius - size *2])
            triangle.add([0.0,radius])
            
             #Create batch white triangle
            w_batch = pyglet.graphics.Batch()
            v1 = w_batch.add(len(triangle.points)//2, GL_LINES, None, ('v2f', triangle.points),('c3f',common.color.white*(len(triangle.points)//2)))
             #Create batch solid yellow triangle
            y_batch = pyglet.graphics.Batch()
            v1 = y_batch.add(len(triangle.points)//2, GL_LINES, None, ('v2f', triangle.points),('c3f',common.color.yellow*(len(triangle.points)//2)))
            v2 = y_batch.add(len(triangle.points)//2, GL_POLYGON, None, ('v2f', triangle.points),('c3f',common.color.yellow*(len(triangle.points)//2)))
            return w_batch, y_batch
    def slip_indicator(self):
    
            radius = 120.0
            size = 8.0
            top = radius - size * 2 -1.0
            
            rect = common.vertex.lines()
            rect.add([-size, top])
            rect.add([-size, top -7.0])
            rect.add([size, top -7.0])
            rect.add([size, top])
            rect.add([-size, top])
            
            w_batch = pyglet.graphics.Batch()
            y_batch = pyglet.graphics.Batch()
            
            v1 = y_batch.add(len(rect.points)//2, GL_LINES, None, ('v2f', rect.points),('c3f',common.color.yellow*(len(rect.points)//2)))
            v3 = y_batch.add(len(rect.points)//2, GL_POLYGON, None, ('v2f', rect.points),('c3f',common.color.yellow*(len(rect.points)//2)))
            v2 = w_batch.add(len(rect.points)//2, GL_LINES, None, ('v2f', rect.points),('c3f',common.color.white*(len(rect.points)//2)))
            
            return w_batch, y_batch
            
            
    def static_triangles(self):
            radius = 120.0
            #glLineWidth(1.5*)
            def bank_ticks(dir):
                def tick(deg, size):
                    #glBegin(GL_LINES)
                    l = []
                    l.extend(common.xycalc.rotate(0.0, radius + size, deg))
                    #glVertex2f(0.0, radius + 12.0)
                    l.extend(common.xycalc.rotate(0.0, radius, deg))
                    #glVertex2f(0.0, radius)
                    #glEnd()
                    return l
                    
                def triang(deg):
                    size = 5.0
                    l = []
                    l.extend(common.xycalc.rotate(0.0, radius, deg))
                    l.extend(common.xycalc.rotate(size, radius+ size *2, deg))
                    l.extend(common.xycalc.rotate(-size, radius+ size *2, deg))
                    l.extend(common.xycalc.rotate(0.0, radius, deg))
                    
                    return l
                    
                #10 deg shorttick
                triangles.reset()
                theta = dir * 10.0
                triangles.add(tick(theta, 12.0))
                #20 deg shorttick
                triangles.reset()
                theta = dir * 20.0
                triangles.add(tick(theta, 12.0))
                #30 deg long tick
                triangles.reset()
                theta = dir * 30.0
                triangles.add(tick(theta, 25.0))
                #45 dig triangle
                triangles.reset()
                theta = dir * 45.0
                triangles.add(triang(theta))
                #60 dig long tick
                triangles.reset()
                theta = dir * 60.0
                triangles.add(tick(theta, 25.0))
                
            #Draw Static triangles
            triangles = common.vertex.lines()
            #Center triangle
            size = 8.0
            triangles.add([0.0,radius, size, radius+ size *2, -size, radius + size *2, 0.0, radius])
            
            #Left side ticks
            bank_ticks(1)
            #Right side ticks
            bank_ticks(-1)
            
            #Create batch
            batch = pyglet.graphics.Batch()
            v1 = batch.add(len(triangles.points)//2, GL_LINES, None, ('v2f', triangles.points),('c3f',common.color.white*(len(triangles.points)//2)))
            
            return batch
    
    def Center_Mark_V(self): #This is one varent of the center mark
    
        def V_shape(side):
            v = common.vertex.lines()
            
            v.add([0.0,0.0])
            v.add([side * 40.0, -30.0])
            v.add([side * 80.0, -30.0])
            v.add([0.0,0.0])
            return v.points, v.list
        
        def Rect(side):
            l = []
            l.extend([-side * 106.0, 2.0])
            l.extend([-side * 106.0, -2.0])
            l.extend([-side * 126.0 , -2.0])
            l.extend([-side * 126.0, 2.0])
            l.extend([-side * 106.0, 2.0])
            return l
            
        v_points = []
        v_points.extend(V_shape(-1)[0])
        v_points.extend(V_shape(1)[0])
        print v_points
        
        v_list = []
        v_list.extend(V_shape(-1)[1])
        v_list.extend(V_shape(1)[1])
        
        rects = common.vertex.lines()
        rects.add(Rect(-1))
        rects.reset()
        rects.add(Rect(1))
        
        fg = pyglet.graphics.OrderedGroup(1)
        fg2= pyglet.graphics.OrderedGroup(2)
        poly = pyglet.graphics.OrderedGroup(0)
        batch = pyglet.graphics.Batch()
        v2 = batch.add(8, GL_POLYGON, poly, ('v2f', v_list),('c3B',(0,0,0)*8))
        v1 = batch.add(len(v_points)//2, GL_LINES, fg, ('v2f', v_points),('c3B',(255,255,255)*(len(v_points)//2)))
        v3 = batch.add(len(rects.points)//2, GL_LINES, fg, ('v2f', rects.points),('c3B',(255,255,255)*(len(rects.points)//2)))
        
        return batch
    
    
    def update(self, dt):
        pass
        #self.pitch += 0.01
        #self.a = 45.0
        #if self.a>180.0:
        #    self.a=-180.0
        #if self.a == -3.0:
        #    self.pitch +=1
        #self.a = 0.0
        #self.pitch = -10.0
    
    def draw(self):
        slope = self.draw_horizon(-self.roll.value,self.pitch.value)
        self.pitch_marks(-self.roll.value, self.pitch.value, 1.5*self.scale_lw)
        
        glLineWidth(1.5*self.scale_lw)
        self.bV_shape.draw()
        self.static_triangle_shape.draw()
        #time.sleep(0.03)
        #self.draw_border()
        #self.pitch.value += 0.2
        #self.roll.value += 0.8
        #if self.pitch.value > 30.0:
        #    self.pitch.value = -30.0
        #if self.roll.value >180.0:
        #    self.roll.value = -180.0
        
            
    def pitch_marks(self, roll, pitch, line_width):
            def get_width(pitch):
                x = int(round(pitch / 2.5))
                if x==0:
                    w = 115 #Horizon is draw during in draw_horizon()
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
            y_center = round(pitch / 2.5) * 2.5
            offset = (y_center -pitch)
            
            y_center = y_center - start_point # Go down 25 degrees
            y = (offset - start_point) * self.pixel_per_degree
            #glTranslatef(0.0, start * pixel_per_degree, 0.0)
            point_l = []
            #print y_center, y, offset
            for i in range(num_lines):
                w = get_width(y_center)
                if w>0:
                    #glBegin(GL_LINES)
                    #glVertex2f(-w, 0.0)
                    #glVertex2f(w, 0.0)
                    #glEnd()
                    point_l.extend([-w,y,w,y])
                if (w==30): #Draw number for degrees
                        glPushMatrix()
                        glTranslatef(35.0, y, 0.0) #Move over to right (Numbers only on right side)
                        glPushMatrix()
                        glScalef(0.12, 0.12, 1.0) #Scale down for numbers
                        text.write(str(int(abs(y_center))))
                        glPopMatrix()
                        glPopMatrix()
                y+=2.5 * self.pixel_per_degree
                #glTranslatef(0.0, 2.5 * pixel_per_degree, 0.0)
                y_center += 2.5
            pyglet.graphics.draw(len(point_l)/2, pyglet.gl.GL_LINES,
                ('v2f', point_l ))    
            if abs(roll)> 30.0:
                self.yellow_triangle.draw()
                #Translation for slip indicator
                glTranslatef(2,0,0)
                self.yellow_slip.draw()
            else:
                self.white_triangle.draw()
                #Translation for slip indicator
                glTranslatef(0,0,0)
                self.white_slip.draw()
                       
            glPopMatrix()
    
    
    def draw_horizon(self, roll, pitch):
        
        def check_side(p1, p2, slope, p3):
            #p1, and p2 will be corners of the Aritifical Horizon
            #p3 is point along horizon line
            #slope is slope of horizon line
            #checking if horizon line intersections a side of the artifical horizon
            p1x = p1[0]
            p1y = p1[1]
            p2x = p2[0]
            p2y = p2[1]
            p3x = p3[0]
            p3y = p3[1]
            
            if p1x == p2x: #Checking a vertical side
                vert = True
            else: #Must be horizontal side
                vert = False
                
            #If verticle solve horizon line where intersects p1x or p2x
            if vert:
                run = p2x - p3x
                y = (slope * run) + p3y
                #y = round(y,0)
                if ((p1y <= y <p2y) or (p2y < y <=p1y)): #Within check
                    return [p1x,int(y)]
                else: 
                    return None
            else: #not vert
                run = p2y - p3y
                if slope ==0: return None
                x = (1.0/slope * run )  + p3x
                #x = round(x,0)
                if ((p1x <= x <p2x) or (p2x < x <=p1x)): #Within check
                    return [int(x),p1y]
                else: 
                    return None
            
        
            
        y = int(-pitch * self.pixel_per_degree / 1)
        rad = math.radians(roll)
        slope = math.tan(rad)
        #Calculate "center" point of horizon
        p3 = [math.sin(-rad)*y, math.cos(-rad)*y]
        middle = [int(p3[0])+5,int(p3[1])+5,int(p3[0])-5,int(p3[1])-5]


        w = 150
        h = 150
        l_points = []
        horizon_cord = []
        corners = [[w,-h],[-w,-h],[-w,h],[w,h]]
        #Determine side intersection
        sides = [[corners[0],corners[1]],[corners[1],corners[2]],[corners[2],corners[3]],[corners[3],corners[0]]]
        
        side_count = 0
        side_hit = [] #List of side, xcord,ycord
        
        count = 0
        for side in sides:
            r = check_side(side[0],side[1],slope,p3)
            
            if r!=None:
                side_hit.append([count,r[0],r[1]])
                side_count +=1
            
            count +=1
        #Take two counts compare cordinates
        reverse = False
        
        if side_count == 2:
            sides_hit = [side_hit[0], side_hit[1]]
            if -45<=roll<=45: #Take right most point
                if side_hit[0][1] < side_hit[1][1]:
                    reverse=True
            elif 45<=roll<=135: #Take upper most point
                if side_hit[0][2] < side_hit[1][2]:
                    reverse=True
            elif -135<=roll<=-45: #Take lower most point
                if side_hit[0][2] > side_hit[1][2]:
                    reverse=True
            else: #Must be take left most point
                if side_hit[0][1] > side_hit[1][1]:
                    reverse=True
            
            if reverse:
                sides_hit = [side_hit[1], side_hit[0]]
       
            #Loope through
            i = sides_hit[0][0] #First side
            l_points.extend([sides_hit[0][1],sides_hit[0][2]])
            
            while i!=sides_hit[1][0]:
                i+=1
                if i==4: i=0
                l_points.extend(corners[i])
            #Last point
            l_points.extend([sides_hit[1][1],sides_hit[1][2]])
            horizon_cord.extend(l_points[:2])
            horizon_cord.extend(l_points[-2:])
        
        #All sky color then draw ground over it.
        pyglet.gl.glColor3f(*self.sky)
        #If pitch is negative and no sides intersect horizon, then screen needs to be all earth.
        if side_count == 0: 
            if pitch<0:
                pyglet.gl.glColor3f(*self.earth)
            
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
            ('v2i', (-w,-h,-w,h,w,h,w,-h)))
        #if (r_side<> l_side):
        #    ps = [lx2,ly2,rx2,ry2]
        #    horz_ps = ps
        #    c_index = r_side
        #    while c_index <> l_side:
        #        ps.append(corners[c_index][0])
        #        ps.append(corners[c_index][1])
        #        c_index+=1
        #        if c_index>3:
        #            c_index = 0
        #    ps.append(lx2)
        #    ps.append(ly2)
        #    #l_side = find_side((lx2,ly2))
        #    #r_side = find_side((rx2,ry2))
        #    #print ps
        pyglet.gl.glColor3f(*self.earth)
        pyglet.graphics.draw(len(l_points)/2, pyglet.gl.GL_POLYGON,
                ('v2i', l_points))
        #    pyglet.gl.glColor3f(1,1,1)
        #pyglet.graphics.draw(len(ps)/2, pyglet.gl.GL_LINES,
        #        ('v2i', horz_ps ))    
        #Draw horizon
        #pyglet.gl.glColor3f(1.0,1.0,1.0)
        #pyglet.graphics.draw(len(horizon_cord)/2, pyglet.gl.GL_LINES,
        #        ('v2i', horizon_cord ))    
        
       
        return slope    
        #self.a+=0.01
        