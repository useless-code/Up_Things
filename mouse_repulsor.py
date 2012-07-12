#!/usr/bin/env python2

##Here is a better example, an yes, the variable names suck. thats me\.::
import pygame
import math
import sys 
import random

from pygame.time import Clock
from pygame import Color, mouse
pygame.init()

circles = set()

tspeed = 1
speed = tspeed
count = 0
n_launchers = 3

def random_color(count):
    color = Color("white")
    color.hsva = (count%360, 90, 80, 60)
    return color

class World(object):
    def __init__(self, x, y, x_accel=0, y_accel=0):
        self.x = x
        self.y = y
        self.center_x = self.x / 2
        self.center_y = self.y / 2
        self.mass = 2.0
        self.points = []
        self.lock = False
        self.color = random_color(60)

    def update(self):
        for x, y, signo in self.points:
            pygame.draw.circle(screen, self.color, (int(x), int(y)), int(10) )

    def calculate_gravity_for_particle(self, particle):

        for x, y, signo in self.points:
            if not particle.deleted:
                self._gravity_to_point(x, y, particle, signo)
            else:
                break

    def add_point(self):
        if not self.lock:
            x, y = pygame.mouse.get_pos()
            
            if pygame.mouse.get_pressed()[0]:
                signo = 1
            else:
                signo = -1

            self.points.append((x, y, signo))
            self.lock = True

    def unlock(self):
        self.lock = False


    def _gravity_to_point(self, x, y, particle, signo ):
        dx = particle.x - x
        dy = particle.y - y
        d = pow(dx, 2) + pow(dy, 2)
        ds = math.sqrt(d)
        force = self._calculate_gravity(d)
        if force is not None:
            force *= signo
            particle.x_accel += force * dx / ds
            particle.y_accel += force * dy / ds
        else:
            particle.delete()

    def _calculate_gravity(self, d):
        if d <= 10:
            force = None
        else:
            force =  int( self.mass) / d
            #force = -1.0 * int( self.mass) / d
        return force


class Circle(object):
    def __init__(self, size, world, x=0, y=0, angle=0, speed=1, color = (0,0,0)):
        self.world = world
        self.color = color
        self.size = size/2
        self.speed_x = math.sin(angle) * speed
        self.speed_y = math.cos(angle) * speed
        self.x_accel = 0
        self.y_accel = 0
        self.x = x
        self.y = y #posicion inicial
        self.deleted=False

    def update(self, screen):
        x_size, y_size = screen.get_size()

        foo = self.world.calculate_gravity_for_particle(self)
        self.speed_x += self.x_accel
        self.speed_y += self.y_accel
        self.x += self.speed_x
        self.y += self.speed_y
        if not ( (0 < self.x and self.x < x_size) and (0 < self.y and self.y < y_size)):
            self.delete()
            return
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size) )
   
    def delete(self):
        if not self.deleted:
            global circles
            circles.remove(self)
            self.deleted = True
        
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
           # self.counter += self.color_change_speed
            self.queue.add(Circle(4, self.world, x=self.x+random.randint(-20, 20), y=self.y, angle=angle, speed=self.mov_speed, color=color))
    
    def change(self):
        if not self.cicles:
            #self.rot_speed = random.uniform(-1, 1)
            self.mov_speed = 1 # random.uniform(1, 10)
            self.cicles = random.randint(500, 1000)
            self.q = 1 # random.randint(1, 6)
        self.rotation += (self.rot_speed % 360)
        self.cicles -= 1


x , y = 800, 600 
screen = pygame.display.set_mode((x, y))
clock = Clock()
world = World(x, y, 0, 0.1)

launchers = []

for n in xrange(1, n_launchers + 1 ):
    launchers.append( Launcher(n * x/ (n_launchers+1), n * y /(n_launchers + 1), world, circles ))
    launchers.append( Launcher(n * x/ (n_launchers+1), n * y /(n_launchers + 1), world, circles ))
    launchers.append( Launcher(n * x/ (n_launchers+1), n * y /(n_launchers + 1), world, circles ))
    launchers.append( Launcher(n * x/ (n_launchers+1), n * y /(n_launchers + 1), world, circles ))
    launchers.append( Launcher(n * x/ (n_launchers+1), n * y /(n_launchers + 1), world, circles ))
    launchers.append( Launcher(n * x/ (n_launchers+1), n * y /(n_launchers + 1), world, circles ))




while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            world.add_point()
        elif event.type == pygame.MOUSEBUTTONUP:
            world.unlock()

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

