import math
import pygame

class Particle(object):
    """Define basic particle"""

    def __init__(self, world, x, y, speed=0, angle=0, accel=1):
        self.x = x
        self.y = y
        self.size_x = 4
        self.size_y = 4
        self.radius = self.size_x / 2
        self.world = world
        self.sin = math.sin(angle)
        self.cos = math.cos(angle)
        self.accel_x = self.sin * accel
        self.accel_y = self.cos * accel
        self.speed_x = self.sin * speed
        self.speed_y = self.cos * speed
        self.angle = angle

    def update(self):
        """Update Particle internal state"""
        self.speed_x += (self.accel_x + self.world.accel_x)
        self.speed_y += (self.accel_y + self.world.accel_y)
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self):
        """Draw particle representation on screen"""
        pygame.draw.circle(self.world.screen, 
                        (255, 255, 255),
                        (int(self.x), int(self.y)),
                        self.radius
                        )

    def on_screen(self):
        on_x = self.x >= (0 - self.size_x) and self.x <= (self.world.size_x + self.size_x)
        on_y = self.y >= (0 - self.size_y) and self.y <= (self.world.size_y + self.size_y)
        return on_x and on_y

        

class ImageParticle(Particle):
    image = pygame.image.load('Python.png')

    def __init__(self, world, x, y, speed=0, angle=0, accel=1):
        super(ImageParticle, self).__init__(world, x, y, speed, angle, accel)
        self.size_x = self.image.get_width()
        self.size_y = self.image.get_height()

    def draw(self):
        self.world.screen.blit(
                        self.image,
                        (int(self.x), int(self.y)),
                        )

class HojaParticle(ImageParticle):
    image = pygame.image.load('hoja.png')

class MenemParticle(ImageParticle):
    image = pygame.image.load('menem.png')

class PerritoParticle(ImageParticle):
    image = pygame.image.load('perrito.png')

