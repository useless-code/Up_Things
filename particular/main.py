import pygame
import sys

from particula import Particle
from world import World
from launcher import Launcher

from pygame.time import Clock

pygame.init()

class App(object):
    def __init__(self):
        self.world = World(1024, 768, 0, 0)
        self.world.sprites = []
        self.clock = Clock()
        self.key_binds = {}
        self.launchers = []
        self.n_launchers = 5
        self.world.update()
        self.update()
        self.create_launchers()

    def run(self):
        while True:
            self.dispatch_events()

            for launcher in self.launchers:
                launcher.update()
            to_keep = []
            for sprite in reversed(self.world.sprites):
                sprite.update()
                sprite.draw()
                if sprite.on_screen():
                    to_keep.append(sprite)
            to_keep.reverse()
            self.world.sprites = to_keep
            self.update()

    def dispatch_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            for key, pressed in enumerate(pygame.key.get_pressed()):
                bind = self.key_binds.get(key)
                if pressed and bind:
                    bind()

    def update(self):
        pygame.display.update()
        self.clock.tick(40)
        self.world.update()

    def watch_for(self, event_type):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == event_type:
                    return event

    def bind_key(self, method):
        event = self.watch_for(pygame.KEYDOWN)
        self.key_binds[event.key] = method

    def get_click_point(self):
        event = self.watch_for(pygame.MOUSEBUTTONUP)
        return event.pos

    def create_launchers(self):
        for n in xrange(0, self.n_launchers):
            font = pygame.font.Font(None, 30)
            self.message(
                "Hace click para establecer el lanzador %d" % n
                )
            x, y = self.get_click_point()
            launcher = Launcher(self.world, x, y)

            self.message("Presiona la tecla de disparo")
            self.bind_key(launcher.trigger)
            self.message("Presiona la tecla de re-roll")
            self.bind_key(launcher.roll)
            self.launchers.append(launcher)

    def message(self, message):
            font = pygame.font.Font(None, 30)
            text = font.render(
                    message,
                    True,
                    (255,255,255)
                )
            self.world.screen.blit(text, (0,0))
            self.update()

if __name__ == '__main__':
    app = App()
    app.run()

