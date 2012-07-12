import pygame
import random
import sys
import math

from pygame.time import Clock
from pygame import Color, Rect

pygame.init()


class World(object):

    def __init__(self, x, y):
        self.screen = pygame.display.set_mode((x, y))


class Scene(object):

    def __init__(self, x, y):
        pass

class Sprite(object):

    def __init__(self, x, y, world):
        self.x = x
        self.y = y
        self.world = world
        self.color = self.random_color()
        self.rect = Rect(self.x, self.y, 20, 20)
        self.drawme = True

    def random_color(self):
        color = Color("white")
        color.hsva = (random.randint(0,350), 90, 80, 60)
        return color


class Bloque(Sprite):

    def draw(self):
        self.rect = Rect(self.x, self.y, 40, 20)
        pygame.draw.rect(self.world.screen, self.color, self.rect)


class Barrita(Sprite):
    def draw(self):
        self.rect = Rect(self.x, self.y, 60, 20)
        pygame.draw.rect(self.world.screen, self.color, self.rect)

    def mover_izq(self):
        self.x -= 3

    def mover_der(self):
        self.x += 3

class Pelota(Sprite):
    def __init__(self, x, y, world):
        self.x = x
        self.y = y
        self.world = world
        self.color = self.random_color()
        self.speed = 4
        self.angle = math.radians(160)
        


    def draw(self):
        self.x += math.sin(self.angle) * self.speed
        self.y += math.cos(self.angle) * self.speed
        self.rect = Rect(self.x, self.y, 20, 20)
        x = int(self.x + 10)
        y = int(self.y + 10)
        pygame.draw.circle(self.world.screen, self.color, (x, y), 10)
    
    def collide(self):
        self.angle = self.angle + math.radians(170)


def main():
    bloques = []
    world = World(800,600)
    clock = Clock()
    for n in xrange(0, 240):
        x = 20 + (n%20) * 40
        y = 20 + (n/20) * 20 
        bloques.append(Bloque(x, y, world))

    barrita = Barrita(400, 500, world)
    pelota = Pelota(400, 300, world)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]: barrita.mover_izq()
        if key[pygame.K_RIGHT]: barrita.mover_der()
        if key[pygame.K_UP]: pelota.collide()
        world.screen.fill((0,0,0))

        barrita.draw()
        pelota.draw()
        collided = True
        if collided and barrita.rect.colliderect(pelota.rect):
            pelota.collide()
            collided = False
        
        for c in bloques:
            if c.drawme:
                if collided and c.rect.colliderect(pelota.rect):
                    pelota.collide()
                    c.drawme = False
                    collided = False
                c.draw()

        collided = True

        pygame.display.update()
        clock.tick(50)

if __name__ == '__main__':
    main()
