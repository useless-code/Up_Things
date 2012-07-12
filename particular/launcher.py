import random
from particula import Particle, ImageParticle, HojaParticle, MenemParticle, PerritoParticle

class Launcher(object):

    def __init__(self, world, x, y, particle=Particle, accel=1):
        self.x = x
        self.y = y
        self.world = world
        self.particle = particle
        self.accel = accel
        self.rotation = 0
        self.roll()

    def roll(self):
        self.rot_speed = random.uniform(-40, 40)
        self.mov_speed = random.uniform(0.001, 1)
        self.accel = random.uniform(-2, 2)
        self.q = random.randint(1, 6)
        self.particle = random.choice([PerritoParticle, Particle, ImageParticle, HojaParticle, MenemParticle])

    def trigger(self):
        for n in xrange(self.q):
            angle = ((n*360.0/self.q) + self.rotation) % 360
            self.world.sprites.append(
                    self.particle(
                        self.world, 
                        x=self.x, 
                        y=self.y, 
                        angle=angle, 
                        speed=self.mov_speed, 
                        accel=self.accel
                        )
                    )

    def update(self):
        self.rotation += (self.rot_speed % 360)



