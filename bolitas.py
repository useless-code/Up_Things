#!/usr/bin/env python2

##Here is a better example, an yes, the variable names suck. thats me\.::
import pygame
import math
import sys 
import random

from pygame.time import Clock
from pygame import Color

pygame.init()

circles = set()

tspeed = 1
speed = tspeed
count = 0
n_launchers = 1

def random_color(count):
    color = Color("white")
    color.hsva = (count%360, 90, 80, 60)
    return color


    
class Circle(object):
    def __init__(self, size, x=0, y=0, angle=0, speed=1, color = (0,0,0)):
        self.color = color
        self.size = size/2
        self.angle = math.radians(angle)
        self.speed = speed
        self.accel = -0.1 
        self.x = x
        self.y = y #posicion inicial

    def update(self, screen):
        global circles
        x_size, y_size = screen.get_size()
        if not ( (0 < self.x and self.x < x_size) and (0 < self.y and self.y < y_size)):
            circles.remove(self)
        self.speed += self.accel
        self.x += math.sin(self.angle) * self.speed
        self.y += math.cos(self.angle) * self.speed
        
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size) )
    
    def __repr__(self):
        return "<Circle (%d, %d) %d>" % (self.x, self.y, self.angle)
        


class Launcher(object):
    
    def __init__(self, x, y, queue):
        self.x = x
        self.y = y
        self.queue = queue
        self.cicles = 0
        self.rot_speed = 0
        self.mov_speed = 0
        self.q = 0
        self.rotation = 0
        self.counter = random.randint(0, 0xFFFFFF)
        self.color_change_speed = random.randint(1,3)

    def explode(self):
        for n in xrange(self.q):
            angle = ((n*360.0/self.q) + self.rotation) % 360
            color = random_color(self.counter)
            self.counter += self.color_change_speed
            self.queue.add(Circle(4, x=self.x, y=self.y, angle=angle, speed=self.mov_speed, color=color))
    
    def change(self):
        if not self.cicles:
            self.rot_speed = random.randint(1, 40) * random.choice([-1, 1])
            self.mov_speed = random.randint(1, 14)
            self.cicles = random.randint(100, 200)
            self.q = random.randint(1, 6)
        self.rotation += (self.rot_speed % 360)
        self.cicles -= 1


x , y = 1024, 500
screen = pygame.display.set_mode((x, y))
clock = Clock()

launchers = []

for n in xrange(0, n_launchers ):
    launchers.append( Launcher(x/2, y/2, circles ))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill((0,0,0))
    circle_list = list(circles)
    for c in circle_list:
        c.update(screen)
    for launcher in launchers:
        launcher.change()
    if len(circles) < 5000:    
        for launcher in launchers:
            launcher.explode()
    
    pygame.display.update()
    clock.tick(50)

