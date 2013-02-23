from pyglet.gl import *

import pyglet
import math

def add_batch(batch, mode, points):
    new_list = []
    #Check for tuples and convert to points in list.
    for p in points:
        if ((type(p) == tuple) or (type(p) == list)):
            for h in p:
                new_list.append(h)
        else:
            new_list.append(p)
            
            
    v = batch.add(len(new_list) // 2, mode, None, ('v2f', new_list))
    return v

class char_c(object):
    #One for each character of text.
    def __init__(self, func):
        self.batch = func()

    def draw(self):
        self.batch.draw()

def draw_0(q=False):
    w = 34
    h = 48
    l = []
    steps = 20
    for i in range(steps):
        angle = 2*3.14159* i / steps
        a = w # + globaltest.one
        b = h # + globaltest.two
        l.append(a*math.cos(angle))
        l.append(b*math.sin(angle))
    
    #For Q only
    x1 = w
    y1 = w
    m = [w,-h, w-x1, -h + y1]
    #glBegin(GL_LINE_LOOP)
    #for t in l:
    #    glVertex2f(t[0],t[1])
    #glEnd()
    batch = pyglet.graphics.Batch()
    v1 = add_batch(batch, GL_LINE_LOOP, l)
    if q:
        v2 = add_batch(batch,GL_LINES, m)
    return batch
def draw_1():
    
    #glTranslate(-10,0,0)
    #glBegin(GL_LINES)
    p = []
    w = 25
    slope = 0.45
    x2 = 46 * slope
    y2 = 46 * (1-slope)
    p.append(-2-x2)
    p.append(50-y2)
    p.append(-2)
    p.append(50)
    p.append(-2)
    p.append(50)
    #glVertex2f(-2,-46)
    p.append(-2)
    p.append(-46)
    #glVertex2f(-w-2,-46)
    p.append(-w-2)
    p.append(-46)
    #glVertex2f(w-2,-46)
    p.append(w-2)
    p.append(-46)
    #Batch
    batch = pyglet.graphics.Batch()
    v = add_batch(batch, GL_LINES, p)
    return batch
    #glEnd()
    
def draw_2():
    steps = 10
    w = 32
    l = []
    for i in range(steps):
        angle = 3.14159* (steps-i) / steps
        r = w
        l.append((r*math.cos(angle), r*math.sin(angle)+16))
    l.append((w,16-4))
    l.append((-w-2, -50+ 18))
    #Bottom line
    l.append((-w-2, -46))
    l.append((w,-46))
    
    #glBegin(GL_LINE_STRIP)
    #for t in l:
    #    glVertex2f(t[0],t[1])
    #glEnd()	
    batch = pyglet.graphics.Batch()
    v = add_batch(batch, GL_LINE_STRIP, l)
    return batch
    
def draw_3():
    steps = 15
    l = []
    m = []
    for i in range(steps):
        start = 2.0 #+ (globaltest.one * 0.1)
        length = -4.9 #+(globaltest.two * 0.1)
        angle = (length* (steps-i) / steps) + start
        a = 32 # + globaltest.one
        b = 26 
        l.append((a*math.cos(angle),b*math.sin(angle)-24))
        
    for i in range(steps):
        start = -2.0 #+ (globaltest.one * 0.1)
        length = 4.9 #+(globaltest.two * 0.1)
        angle = (length* (steps-i) / steps) + start
        a = 28  #+ globaltest.one
        b = 22 
        m.append((a*math.cos(angle),b*math.sin(angle)+25))
    
    batch = pyglet.graphics.Batch()
    #glBegin(GL_LINE_STRIP)
    #for t in l:
    #    glVertex2f(t[0],t[1])
    #glEnd()	
    v1 = add_batch(batch, GL_LINE_STRIP, l)
    #glBegin(GL_LINE_STRIP)
    #for t in m:
    #    glVertex2f(t[0],t[1])
    #glEnd()	
    m.reverse()
    v2 = add_batch(batch, GL_LINE_STRIP, m)
    
    return batch
    
def draw_4():
    
    #glBegin(GL_LINES)
    p = []
    w = 34
    x1 = 10
    slope = 1.5
    y2 = slope * (-w -x1)
    
    p.append((x1,50))
    p.append((-w,50+y2))
    p.append((-w,50+y2))
    p.append((w,50+y2))
    p.append((x1,-52))
    p.append((x1,20))
    #glEnd()
    batch = pyglet.graphics.Batch()
    v = add_batch(batch, GL_LINES, p)
    return batch
    
    
def draw_5():
    steps = 15
    l = []
    for i in range(steps):
        start = 3.0 #+ (globaltest.one * 0.1)
        length = -5.6 #+(globaltest.two * 0.1)
        angle = (length* (steps-i) / steps) + start
        a = 36 #+ globaltest.one
        b = 33 #+ globaltest.two
        l.append((a*math.cos(angle)-3,b*math.sin(angle)-18))
        
    #glBegin(GL_LINE_STRIP)
    #for t in l:
    #    glVertex2f(t[0],t[1])
        #print l
    l.append((-34,-1))
    l.append((-34,46))
    l.append((34,46))
    
    #glEnd()	
    batch = pyglet.graphics.Batch()
    v = add_batch(batch, GL_LINE_STRIP, l)
    return batch
    
def draw_6():
    return draw_69(6)

def draw_9():
    return draw_69(9)

def draw_69(num):
    steps = 16
    l = []
    m = []
    for i in range(steps):
        angle = (2*3.14159* (i-2) / (steps -1)) + 180
        a = 33# + globaltest.one
        b = 28# + globaltest.two
        l.append((a*math.cos(angle),b*math.sin(angle)-22))
        
    for i in range(steps):
        start = 0.4  #+ (globaltest.two * 0.1)
        length = 2.7 #-(globaltest.two * 0.1)
        angle = (length* (i) / steps) + start
        a = 29 #+ globaltest.two
        b = 22 #+ globaltest.two
        m.append((a*math.cos(angle)+ 5,b*math.sin(angle)+25))
    #Add smooth
    m.append((-29,14))
    m.append((-33,-18))
    m.reverse()
    if num == 9:
        m = [(-x[0],-x[1]) for x in m]
        l = [(-x[0],-x[1]) for x in l]
        

    #glBegin(GL_LINE_LOOP)
    #for t in l:
    #    glVertex2f(t[0],t[1])
    #glEnd()	
    #glBegin(GL_LINE_STRIP)
    #for t in m:
    #    glVertex2f(t[0],t[1])
    #glVertex2f(-29+globaltest.one,14+globaltest.two)	
    #glVertex2f(-33,-18)	
    
    #glEnd()	
    #print m
    batch = pyglet.graphics.Batch()
    v1 = add_batch(batch, GL_LINE_STRIP, l)
    v2 = add_batch(batch, GL_LINE_STRIP, m)
    return batch
    

def draw_7():
    
    l = []
    w = 34
    h = 50
    #glBegin(GL_LINE_STRIP)
    l.append((-w,h-6))
    l.append((w,h-6))
    l.append((-w+6,-h))
    
    #glEnd()	
    batch = pyglet.graphics.Batch()
    v = add_batch(batch, GL_LINE_STRIP, l)
    return batch


def draw_8():
    steps = 16
    l = []
    m = []
    for i in range(steps):
        angle = (2*3.14159* (i-1) / (steps-1)) + 90
        a = 32 # + globaltest.one
        b = 26 #+ globaltest.two
        l.append((a*math.cos(angle),b*math.sin(angle)-24))
        
    for i in range(steps):
        angle = (2*3.14159* (i+1) / (steps-1)) - 90
        a = 26  #+ globaltest.one
        b = 23  
        m.append((a*math.cos(angle),b*math.sin(angle)+26))
    
    #glBegin(GL_LINE_LOOP)
    #for t in l:
    #    glVertex2f(t[0],t[1])
    #glEnd()	
    #glBegin(GL_LINE_LOOP)
    #for t in m:
    #    glVertex2f(t[0],t[1])
    #glEnd()	
    batch = pyglet.graphics.Batch()
    v1 = add_batch(batch, GL_LINE_STRIP, l)
    v2 = add_batch(batch, GL_LINE_STRIP, m)
    return batch
    
def draw_A():   
    w = 34
    h = 50
    slope = 34 / 100.0
    points = [-w,-h,0,h,0,h,w,-h]
    y = -8
    x = (50 - y) * slope
    points.append([-x,y,x,y])
    batch = pyglet.graphics.Batch()
    #v = batch.add(4, GL_LINES, None, ('v2f', (-w,h,0,-h,0,-h,w,h)))
    v = add_batch(batch, GL_LINES, points)
    
    return batch

def draw_B():   
    steps = 15
    w = 34
    h = 50
    y = 5 #center of "B"
    m = []
    x3 = -2
    m.append((-w,y))
    m.append((x3,y))
    for i in range(steps):
        angle = (1*3.14159* (i) / (steps-1)) - (3.14159/2)
        a = 57-34-x3  #+ globaltest.one
        b = (h - y) / 2  
        m.append((a*math.cos(angle)+x3,b*math.sin(angle)+(b+y)))
    m.append((x3,h))
    m.append((-w,h))
    m.append((-w,-h))
    m.append((x3,-h))
    for i in range(steps):
        angle = (1*3.14159* (i) / (steps-1)) - (3.14159/2)
        a = 60-34-x3  #+ globaltest.one
        b = (y + h ) /2  
        m.append((a*math.cos(angle)+x3,b*math.sin(angle)+(-h+b)))
    
    batch = pyglet.graphics.Batch()
    #v = batch.add(4, GL_LINES, None, ('v2f', (-w,h,0,-h,0,-h,w,h)))
    v = add_batch(batch, GL_LINE_STRIP, m)
    
    return batch

def draw_C():
    l = []
    steps = 15
    start = 0.6
    length = 2*3.14159 - (start*2)
    for i in range(steps):
        angle = (length* (i) / (steps-1)) + start
        a = 37 # + globaltest.one
        b = 50 # + globaltest.two
        x_offset = (a - 34)
        l.append(a*math.cos(angle)+ x_offset)
        l.append(b*math.sin(angle))
    
    #glBegin(GL_LINE_LOOP)
    #for t in l:
    #    glVertex2f(t[0],t[1])
    #glEnd()
    batch = pyglet.graphics.Batch()
    v = add_batch(batch, GL_LINE_STRIP, l)
    return batch

def draw_D():
    m = []
    h = 50
    w = 34
    x3 = -14
    steps = 15
    start = -3.14159/2
    length = 3.14159
    m.append((x3,h))
    m.append((-w,h))
    m.append((-w,-h))
    m.append((x3,-h))
    for i in range(steps):
        angle = (1*3.14159* (i) / (steps-1)) - (3.14159/2)
        a = 68-34-x3  #+ globaltest.one
        b =  h  
        m.append((a*math.cos(angle)+x3,b*math.sin(angle)+(-h+b)))
    #print m
    #glBegin(GL_LINE_LOOP)
    #for t in l:
    #    glVertex2f(t[0],t[1])
    #glEnd()
    batch = pyglet.graphics.Batch()
    v = add_batch(batch, GL_LINE_STRIP, m)
    return batch

def draw_E():
    w = 34
    h = 50
    m = []
    x1 = 15
    y1 = 7
    m.append([-w,h,w,h,-w,h,-w,-h,-w,-h,w,-h])
    m.append([-w,y1,x1,y1])
    #points.append([-x,y,x,y])
    batch = pyglet.graphics.Batch()
    #v = batch.add(4, GL_LINES, None, ('v2f', (-w,h,0,-h,0,-h,w,h)))
    v = add_batch(batch, GL_LINES, m)
    
    return batch

def draw_F():
    w = 34
    h = 50
    m = []
    x1 = 15
    y1 = 0
    m.append([-w,h,w,h,-w,h,-w,-h])
    m.append([-w,y1,x1,y1])
    #points.append([-x,y,x,y])
    batch = pyglet.graphics.Batch()
    #v = batch.add(4, GL_LINES, None, ('v2f', (-w,h,0,-h,0,-h,w,h)))
    v = add_batch(batch, GL_LINES, m)
    
    return batch

def draw_G():
    m = []
    h = 50
    w = 34
    y1 = -8
    x1 = -5
    steps = 12
    start = -3.14159/2
    length = 3.14159
    m.append((x1,y1))
    m.append((w,y1))
    #Lower circle
    for i in range(steps):
        angle = (1*3.14159* (-i) / (steps-1))
        a = 34  #+ globaltest.one
        b =  h + y1
        m.append((a*math.cos(angle),b*math.sin(angle)+(-h+b)))
    #print m
    #Upper Circle
    length = -3.14159 / 2
    start = -3.14159
    for i in range(steps):
        angle = (length * i / (steps-1)) + start
        a = 40
        b = 50 - y1
        x_offset = a - 34
        m.append((a*math.cos(angle)+x_offset,b*math.sin(angle)+y1))
    
    start = start+length
    length = -0.55
    for i in range(steps):
        angle = (length * i / (steps-1)) + start
        a = 44
        b = 50 - y1
        x_offset = a - 34
        m.append((a*math.cos(angle)+x_offset,b*math.sin(angle)+y1))
    #print m
    batch = pyglet.graphics.Batch()
    v = add_batch(batch, GL_LINE_STRIP, m)
    return batch

def draw_H():
    w = 32
    h = 50
    m = []
    y1 = 7
    m.append([-w,h,-w,-h,w,h,w,-h,-w,y1,w,y1])
    
    #points.append([-x,y,x,y])
    batch = pyglet.graphics.Batch()
    #v = batch.add(4, GL_LINES, None, ('v2f', (-w,h,0,-h,0,-h,w,h)))
    v = add_batch(batch, GL_LINES, m)
    
    return batch

def draw_I():
    w = 32
    h = 48
    m = []
    w1 = 17
    m.append([-w1,h,w1,h,0,h,0,-h,-w1,-h,w1,-h])
    
    #points.append([-x,y,x,y])
    batch = pyglet.graphics.Batch()
    #v = batch.add(4, GL_LINES, None, ('v2f', (-w,h,0,-h,0,-h,w,h)))
    v = add_batch(batch, GL_LINES, m)
    
    return batch

def draw_J():
    m = []
    h = 50
    w = 32
    y1 = -8
    x1 = w
    steps = 12
    start = -3.14159/2
    length = 3.14159
    
    m.append((x1,h))
    m.append((x1,y1))
   
    #Lower circle
    for i in range(steps):
        angle = (1*3.14159* (-i) / (steps-1))
        a = w  #+ globaltest.one
        b =  h + y1
        m.append((a*math.cos(angle),b*math.sin(angle)+(-h+b)))
    #print m
   
    batch = pyglet.graphics.Batch()
    v = add_batch(batch, GL_LINE_STRIP, m)
    return batch
def draw_K():
    
    w = 32
    h = 50
    m = []
    y1 = -7
    m.append([-w,h,-w,-h,w,h,-w,y1])
    y2 = 7
    slope = (50 - y1) / (2.0*w)
    #y = mx +b 
    b = h - slope * w
    
    x2 = -w + 10
    y2 = x2*slope + b
    
    
    m.append([x2,y2,w,-h])
    #points.append([-x,y,x,y])
    batch = pyglet.graphics.Batch()
    #v = batch.add(4, GL_LINES, None, ('v2f', (-w,h,0,-h,0,-h,w,h)))
    v = add_batch(batch, GL_LINES, m)
    
    return batch

def draw_L():
    w = 32
    h = 48
    m = []
    m.append([-w,h,-w,-h,-w,-h,w,-h])
    
    #points.append([-x,y,x,y])
    batch = pyglet.graphics.Batch()
    #v = batch.add(4, GL_LINES, None, ('v2f', (-w,h,0,-h,0,-h,w,h)))
    v = add_batch(batch, GL_LINES, m)
    
    return batch

def draw_M():
    w = 32
    h = 50
    m = []
    x1 = 0
    y1 = -7
    m.append([-w,-h,-w,h,x1,y1,w,h,w,-h])
    
    #points.append([-x,y,x,y])
    batch = pyglet.graphics.Batch()
    #v = batch.add(4, GL_LINES, None, ('v2f', (-w,h,0,-h,0,-h,w,h)))
    v = add_batch(batch, GL_LINE_STRIP, m)
    
    return batch

def draw_N():
    w = 32
    h = 50
    m = []
    m.append([-w,-h,-w,h,w,-h,w,h])
    
    #points.append([-x,y,x,y])
    batch = pyglet.graphics.Batch()
    #v = batch.add(4, GL_LINES, None, ('v2f', (-w,h,0,-h,0,-h,w,h)))
    v = add_batch(batch, GL_LINE_STRIP, m)
    
    return batch

def draw_P():
    return draw_PR(False)

def draw_Q():
    return draw_0(q=True)

def draw_R():
    return draw_PR(True)

def draw_PR(r):
    steps = 15
    w = 34
    h = 50
    y = 0 #center of "B"
    m = []
    x3 = -2
    m.append((-w,y))
    m.append((x3,y))
    for i in range(steps):
        angle = (1*3.14159* (i) / (steps-1)) - (3.14159/2)
        a = 68-34-x3  #+ globaltest.one
        b = (h - y) / 2  
        m.append((a*math.cos(angle)+x3,b*math.sin(angle)+(b+y)))
    m.append((x3,h))
    m.append((-w,h))
    m.append((-w,-h))
    l = [x3,y,w,-h]
    #for i in range(steps):
    #    angle = (1*3.14159* (i) / (steps-1)) - (3.14159/2)
    #    a = 60-34-x3  #+ globaltest.one
    #    b = (y + h ) /2  
    #    m.append((a*math.cos(angle)+x3,b*math.sin(angle)+(-h+b)))
    
    batch = pyglet.graphics.Batch()
    #v = batch.add(4, GL_LINES, None, ('v2f', (-w,h,0,-h,0,-h,w,h)))
    v1 = add_batch(batch, GL_LINE_STRIP, m)
    if r:
        v2 = add_batch(batch, GL_LINES, l)
    
    return batch

def draw_S():
    w = 32
    h = 50
    x = 68
    y = 90
    p = []
    m = [72,23,62,19,52,16,40,16,28,19,19,24,14,31,13,40,20,47,34,54,48,60,58,66,65,72,68,80,67,88,64,94,58,100,48,103,36,103,24,102,14,99,6,94]
    #print "RANGE",range(0,len(m),2)
    for i in range(0,len(m),2):
        p.append(1.0*(m[i]-4)/x*w*2-w)
        p.append(-1.0*(m[i+1]-15)/y*h*2+h)
        
    batch = pyglet.graphics.Batch()
    #v = batch.add(4, GL_LINES, None, ('v2f', (-w,h,0,-h,0,-h,w,h)))
    v1 = add_batch(batch, GL_LINE_STRIP, p)
    
    return batch

def draw_T():
    w = 32
    h = 48
    m = []
    m.append([-w,h,w,h,0,h,0,-(h+2)])
    
    #points.append([-x,y,x,y])
    batch = pyglet.graphics.Batch()
    #v = batch.add(4, GL_LINES, None, ('v2f', (-w,h,0,-h,0,-h,w,h)))
    v = add_batch(batch, GL_LINES, m)
    
    return batch

def draw_U():
    m = []
    h = 50
    w = 32
    y1 = -8
    x1 = w
    steps = 12
    start = -3.14159/2
    length = 3.14159
    
    m.append((x1,h))
    m.append((x1,y1))
   
    #Lower circle
    for i in range(steps):
        angle = (1*3.14159* (-i) / (steps-1))
        a = w  #+ globaltest.one
        b =  h + y1
        m.append((a*math.cos(angle),b*math.sin(angle)+(-h+b)))
    #print m
    m.append((-x1,y1))
    m.append((-x1,h))
    
    batch = pyglet.graphics.Batch()
    v = add_batch(batch, GL_LINE_STRIP, m)
    return batch


def draw_V():
    w = 34
    h = 50
    points = [-w,h,0,-h,0,-h,w,h]
    batch = pyglet.graphics.Batch()
    #v = batch.add(4, GL_LINES, None, ('v2f', (-w,h,0,-h,0,-h,w,h)))
    v = add_batch(batch, GL_LINES, points)
    
    return batch

def draw_W():
    w = 34
    h = 50
    m = []
    x1 = 0
    x_offset = 10
    y1 = 5
    m.append([-w,h])
    m.append([-(w-x_offset),-h])
    m.append([x1,y1])
    m.append([w-x_offset,-h])
    m.append([w,h])
    
    #points.append([-x,y,x,y])
    batch = pyglet.graphics.Batch()
    #v = batch.add(4, GL_LINES, None, ('v2f', (-w,h,0,-h,0,-h,w,h)))
    v = add_batch(batch, GL_LINE_STRIP, m)
    
    return batch

def draw_X():
    w = 34
    h = 50
    m = []
    x1 = 0
    x_offset = 10
    y1 = 5
    m.append([-w,h,w,-h])
    m.append([-w,-h,w,h])
    
    #points.append([-x,y,x,y])
    batch = pyglet.graphics.Batch()
    #v = batch.add(4, GL_LINES, None, ('v2f', (-w,h,0,-h,0,-h,w,h)))
    v = add_batch(batch, GL_LINES, m)
    
    return batch

def draw_Y():
    w = 34
    h = 50
    m = []
    x1 = 0
    x_offset = 10
    y1 = 5
    m.append([-w,h,0,0])
    m.append([w,h,0,0])
    m.append([0,0,0,-h])
    
    
    #points.append([-x,y,x,y])
    batch = pyglet.graphics.Batch()
    #v = batch.add(4, GL_LINES, None, ('v2f', (-w,h,0,-h,0,-h,w,h)))
    v = add_batch(batch, GL_LINES, m)
    
    return batch

def draw_Z():
    w = 34
    h = 48
    m = []
    x1 = 0
    x_offset = 10
    y1 = 5
    m.append([-w,h,w,h])
    m.append([w,h,-w,-h])
    m.append([-w,-h,w,-h])
    
    
    #points.append([-x,y,x,y])
    batch = pyglet.graphics.Batch()
    #v = batch.add(4, GL_LINES, None, ('v2f', (-w,h,0,-h,0,-h,w,h)))
    v = add_batch(batch, GL_LINES, m)
    
    return batch

def draw_period():
    x = -34-7
    y = -48
    w = 7
    h = 7
    m = []
    x1 = 0
    x_offset = 10
    y1 = 5
    for i in range(w):
        m.append([x,y+i,x+w,y+i])
       
    
    #points.append([-x,y,x,y])
    batch = pyglet.graphics.Batch()
    #v = batch.add(4, GL_LINES, None, ('v2f', (-w,h,0,-h,0,-h,w,h)))
    v = add_batch(batch, GL_LINES, m)
    
    return batch

def draw_dash():
    x = 34
    y_list = [-1,0,1]
    m = []
    
    for y in y_list:
        m.append([x,y,-x,y])
       
    
    #points.append([-x,y,x,y])
    batch = pyglet.graphics.Batch()
    #v = batch.add(4, GL_LINES, None, ('v2f', (-w,h,0,-h,0,-h,w,h)))
    v = add_batch(batch, GL_LINES, m)
    
    return batch


dict = {}
dict[' '] = None
dict['0'] = char_c(draw_0)
dict['1'] = char_c(draw_1)
dict['2'] = char_c(draw_2)
dict['3'] = char_c(draw_3)
dict['4'] = char_c(draw_4)
dict['5'] = char_c(draw_5)
dict['6'] = char_c(draw_6)
dict['7'] = char_c(draw_7)
dict['8'] = char_c(draw_8)
dict['9'] = char_c(draw_9)
dict['A'] = char_c(draw_A)
dict['B'] = char_c(draw_B)
dict['C'] = char_c(draw_C)
dict['D'] = char_c(draw_D)
dict['E'] = char_c(draw_E)
dict['F'] = char_c(draw_F)
dict['G'] = char_c(draw_G)
dict['H'] = char_c(draw_H)
dict['I'] = char_c(draw_I)
dict['J'] = char_c(draw_J)
dict['K'] = char_c(draw_K)
dict['L'] = char_c(draw_L)
dict['M'] = char_c(draw_M)
dict['N'] = char_c(draw_N)
dict['O'] = char_c(draw_0)
dict['P'] = char_c(draw_P)
dict['Q'] = char_c(draw_Q)
dict['R'] = char_c(draw_R)
dict['S'] = char_c(draw_S)
dict['T'] = char_c(draw_T)
dict['U'] = char_c(draw_U)
dict['V'] = char_c(draw_V)
dict['W'] = char_c(draw_W)
dict['X'] = char_c(draw_X)
dict['Y'] = char_c(draw_Y)
dict['Z'] = char_c(draw_Z)
dict['.'] = char_c(draw_period)
dict['-'] = char_c(draw_dash)
#v = char_c(draw_9)

def write(s, spacing = 85):
    #len_s = len(s)
    #count  = 0
    for c in s:
        space = spacing
        if dict[c]:
            dict[c].draw()
            if c=='.':
                space -= 75
        #count+=1
        #if count != len_s: #Move to next character if not last one.
        glTranslatef(space,0,0)
                
        
