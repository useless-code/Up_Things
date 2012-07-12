import pygame

class World(object):
    def __init__(self, x, y, accel_x=0, accel_y=0):
        self.screen = pygame.display.set_mode((x, y))
        self.size_x = x
        self.size_y = y
        self.accel_x = accel_x
        self.accel_y = accel_y

    def update(self):
        self.screen.fill((0,0,0))


