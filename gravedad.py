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
n_launchers = 6

def random_color(count):
    color = Color("white")
    color.hsva = (count%360, 90, 80, 60)
    return color

class World(object):
    def __init__(self, x_accel=0, y_accel=0):
        self.x_accel = x_accel
        self.y_accel = y_accel
        self.cicles = 200
    
    def update(self):
        if not self.cicles:
            self.cicles = random.randint(100, 200)
            self.x_accel = random.uniform(-1, 1)
            self.y_accel = random.uniform(-1, 1)
        self.cicles -= 1


class Circle(object):
    def __init__(self, size, world, x=0, y=0, angle=0, speed=1, color = (0,0,0)):
        self.world = world
        self.color = color
        self.size = size/2
        self.speed_x = math.sin(angle) * speed
        self.speed_y = math.cos(angle) * speed
        self.accel_x = 0
        self.accel_y = 1
        self.x = x
        self.y = y #posicion inicial

    def update(self, screen):
        global circles
        x_size, y_size = screen.get_size()
        if not ( (0 < self.x and self.x < x_size) and (0 < self.y and self.y < y_size)):
            circles.remove(self)
        self.speed_x += self.world.x_accel
        self.speed_y += self.world.y_accel
        self.x += self.speed_x
        self.y += self.speed_y
        
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size) )
    
    def __repr__(self):
        return "<Circle (%d, %d) %d>" % (self.x, self.y, self.angle)
        


class Launcher(object):
    
    def __init__(self, x, y, world, queue):
        self.x = x
        self.y = y
        self.world = world
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
            self.queue.add(Circle(4, self.world, x=self.x, y=self.y, angle=angle, speed=self.mov_speed, color=color))
    
    def change(self):
        if not self.cicles:
            self.rot_speed = random.randint(1, 40) * random.choice([-1, 1])
            self.mov_speed = random.randint(1, 14)
            self.cicles = random.randint(100, 200)
            self.q = random.randint(1, 6)
        self.rotation += (self.rot_speed % 360)
        self.cicles -= 1


x , y = 1024, 768
screen = pygame.display.set_mode((x, y))
clock = Clock()
world = World(0, 0.1)

launchers = []

for n in xrange(0, n_launchers ):
    launchers.append( Launcher(x/2, y/2, world, circles ))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill((0,0,0))
    circle_list = list(circles)
    world.update()
    for c in circle_list:
        c.update(screen)
    for launcher in launchers:
        launcher.change()
    if len(circles) < 5000:    
        for launcher in launchers:
            launcher.explode()
    
    
    pygame.display.update()
    clock.tick(50)

