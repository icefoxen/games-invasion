# Not to be confused with Pygame sprites, which are not quite the same!
# Should also probably use the resource loader so we don't make a mojillion rotozoomed copies

#import pygame
#from pygame.locals import *

import sdl2

import math

import resource
import vec

TWOPI = math.pi * 2.0
PIOVER2 = math.pi / 2.0

NUMROTS = 128

class Sprite(object):
    def __init__(s, img):
        s.img = resource.getImage(img)
        s.rots = []
        for i in range(NUMROTS):
            rz = pygame.transform.rotozoom(s.img, -((i / float(NUMROTS)) * 360.0), 1.0)
            s.rots.append(rz)

    # XXX: The height is not really 100% correct...
    def draw(s, surf, gs, loc, angle):
        angle = (angle + PIOVER2) % TWOPI
        sc = gs.screenCoords(loc)
        ang = int((angle / TWOPI) * NUMROTS)
        (w,h) = s.rots[ang].get_size()
        w = w / 2
        h = h / 2
        sc = vec.sub(sc, vec.new(w, h))
        #surf.blit(s.img, sc)
        surf.blit(s.rots[ang], sc)
