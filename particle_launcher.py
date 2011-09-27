##Here is a better example, an yes, the variable names suck. thats me\.::
import pygame
import math
from pygame.time import Clock
import random
pygame.init()

circles = set()

tspeed = 1
speed = tspeed
count = 0

def random_color():
    global count
    r = count % 0xF * 10 
    g = int((count / 0x10) % 0xF) * 10
    b = int((count / 0x100) % 0xF) * 10
    count += 1
    #r = random.randint(10, 255)
    #g = random.randint(10, 255)
    #b = random.randint(10, 255)
    return (r, g, b)

    
class Circle(object):
    def __init__(self, size, x=0, y=0, angle=0, speed=1):
        self.color = random_color()
        self.size = size/2
        self.angle = math.radians(angle)
        self.speed = speed
        self.x = x
        self.y = y #posicion inicial

    def update(self, screen):
        global circles
        pos = (self.x, self.y)
        limit = screen.get_size()
        if pos > limit or pos < (0, 0):
            circles.remove(self)
        self.x += math.sin(self.angle) * self.speed
        self.y += math.cos(self.angle) * self.speed
        if speed > 5:
            self.size += (speed / 2.0)   
        
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size) )
    
    def __repr__(self):
        return "<Circle (%d, %d) %d>" % (self.x, self.y, self.angle)
        

screen = pygame.display.set_mode((1024,768))

def explode(circles, rotation, q, mov_speed):
    #q =  70 #random.randint(0, 100) 
    for n in xrange(q):
        angle = ((n*360.0/q) + rotation) % 360
        circles.add(Circle(5, x=512, y=384, angle=angle, speed=mov_speed))

clock = Clock()
rotation = 0
cicles = 0
while True:
    if not cicles:
        rot_speed = random.randint(1, 40)
        mov_speed = random.randint(1, 14)
        cicles = random.randint(100, 200)
        q = random.randint(1, 6)
        print rot_speed, mov_speed, cicles, q
    cicles -= 1
    screen.fill((0,0,0))
    circle_list = list(circles)
    for c in circle_list:
        c.update(screen)
    if len(circles) < 10000:
        explode(circles, rotation, q, mov_speed)
    rotation += rot_speed
    pygame.display.update()
    clock.tick(50)
