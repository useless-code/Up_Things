import os
import sys
import select
import pygame

WIDTH = 640
HEIGHT = 480

pygame.init()

fpsClock = pygame.time.Clock()

window = pygame.display.set_mode((WIDTH, HEIGHT))

black = pygame.Color(0, 0, 0)
gray = pygame.Color(128, 128, 128)
white = pygame.Color(255, 255, 255)
green = pygame.Color(0, 255, 0)
red = pygame.Color(255, 0, 0)
blue = pygame.Color(0, 0, 255)
pink = pygame.Color(255, 0, 255)
darkGreen = pygame.Color(0, 128, 0)
darkRed = pygame.Color(128, 0, 0)
darkBlue = pygame.Color(0, 0, 128)
darkPink = pygame.Color(128, 0, 128)

intervalColors = [
    blue,   # octave
    red,    # 2nd m
    pink,   # 2nd M
    green,  # 3rd m
    green,  # 3rd M
    blue,   # 4th P
    red,    # 4th A/5th D
    blue,   # 5th P
    green,  # 6th m
    green,  # 6th M
    pink,   # 7th m
    red,    # 7th M
]

inactiveColors = [
    darkBlue,   # octave
    darkRed,    # 2nd m
    darkPink,   # 2nd M
    darkGreen,  # 3rd m
    darkGreen,  # 3rd M
    darkBlue,   # 4th P
    darkRed,    # 4th A/5th D
    darkBlue,   # 5th P
    darkGreen,  # 6th m
    darkGreen,  # 6th M
    darkPink,   # 7th m
    darkRed,    # 7th M
]

fd = os.open('/dev/midi1', os.O_RDONLY)
poll = select.poll()

poll.register(fd, select.POLLIN)

step = 0
notes = []

def add_intervals(new_note):
    for n in notes:
        if n.active:
            n.intervals.append(new_note)

class Note(object):
    def __init__(self, step, pitch):
        self.pitch = pitch
        self.step = step
        self.active = True
        self.intervals = []

    def x(self):
        return WIDTH - (step - self.step)

    def y(self):
        return HEIGHT - 4 * self.pitch


while True:
    step = step + 1
    data = poll.poll(0)
    while data:
        code = ord(os.read(fd, 1))
        if code in (144, 128):
            pitch, force = [ord(x) for x in os.read(fd, 2)]
            if code == 144:
                new_note = Note(step, pitch)
                notes.append(new_note)
                add_intervals(new_note)
            else:
                # !!Use a dict for pitches
                for n in notes:
                    if n.pitch == pitch:
                        n.active = False
        data = poll.poll(0)
    notes = [x for x in notes if x.step > step - WIDTH]
    window.fill(black)
    for n in notes:
        color = white if n.active else gray
        pygame.draw.circle(window, color, (n.x(), n.y()), 2)
        for other in n.intervals:
            if n.active and other.active:
                colorArray = intervalColors
            else:
                colorArray = inactiveColors
            color = colorArray[(other.pitch - n.pitch) % 12]
            pygame.draw.line(window, color, (n.x(), n.y()),
                             (other.x(), other.y()), 1)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    fpsClock.tick(30)
