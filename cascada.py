import random
import numpy as np
import math
import pygame
import sys
from pygame.time import Clock
from particular.world import World

pygame.init()

class WaterFall(object):

    def __init__(self, world, x, y, angle=0, size=30, ttl=0, flow=10, speed=5):
        self.world = world
        self.x = x
        self.y = y
        self.angle = math.radians(angle)
        self.size = size
        self.ttl = ttl
        self.flow = flow
        self.delta_x = math.cos(angle)
        self.delta_y = math.sin(angle)

        self.speed = speed
        self.particles = []
        self.speeds = []

    def update(self):

        if self.particles:
            particles = np.array(self.particles)
            speeds = np.array(self.speeds) + (self.world.accel_x, self.world.accel_y)
            particles += speeds
            self.particles = particles.tolist()
            self.speeds = speeds.tolist()

        self.create_particles()
        self.draw()

    def draw(self):
        to_keep_particles = []
        to_keep_speeds = []
        for index, cords in enumerate(self.particles):
            x, y = cords
            if self.on_screen(x, y):
                pygame.draw.circle(
                    self.world.screen,
                    pygame.Color("white"),
                    (int(x), int(y)),
                    2 )
                to_keep_particles.append(cords)
                to_keep_speeds.append(self.speeds[index])

        self.particles = to_keep_particles
        self.speeds = to_keep_speeds

    def on_screen(self, x, y):
        on_x = x >= 0 and x <= (self.world.size_x)
        on_y = y >= 0 and y <= (self.world.size_y)
        return on_x and on_y


    def create_particles(self):

        for i in xrange(self.flow):
            self.new_particle()

    def new_particle(self):
        x = self.x
        y = self.y

        out_pos = random.randint(- self.size//2, self.size//2)

        x = self.x + out_pos * self.delta_y
        y = self.y + out_pos * self.delta_x

        speed = self.speed + random.uniform(-0.1, 0.1)
        vx = speed * (self.delta_x + random.uniform(-0.1, 0.1))
        vy = speed * (self.delta_y + random.uniform(-0.1, 0.1))

        self.particles.append([x, y])
        self.speeds.append([vx, vy])

class App(object):
    def __init__(self):
        self.world = World(1024, 768, 0, -0.1)
        self.clock = Clock()
        self.update()
        self.waterfall = WaterFall(self.world, self.world.size_x/2, self.world.size_y/2, angle=0)

    def run(self):
        while True:
            self.dispatch_events()
            self.waterfall.update()
            self.update()

    def update(self):
        pygame.display.update()
        self.clock.tick(30)
        self.world.update()

    def dispatch_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()


if __name__ == '__main__':
    app = App()
    app.run()

