#import pygame
#from pygame.locals import *

import sdl2
#import sdl2.sdlimage
import sdl2.ext

import os

#RES = sdl2.ext.Resources(__file__, 'data')

def loadImage(name):
    a = sdl2.ext.load_image(os.path.join("images", name) + ".png")
    return 

def loadSound(name):
    a = pygame.mixer.Sound(os.path.join("sound", name) + ".ogg")
    return a

# ...fuck I'm going to have to rotate sprites.
# Well I have a few options here:
# 1) Pre-rotate a bunch in or inkscape, load the right ones.
# 2) Rotozoom a base sprite.
# Really I'm probably best off doing #1...  Shit that's going
# to take forever.  D:
# 64 rotations will probably look okay though...
# I could probably write a program to do #2 for me; that's easy enough.
# But it will probably look like ass.
# Size changes can be handled just by always calculating coordinates from
# the CENTER of the sprite.
IMAGES = {}
def getImage(name):
    if IMAGES.has_key(name):
        return IMAGES[name]
    else:
        a = loadImage(name)
        IMAGES[name] = a
        return a



SPRITES = {}
def getSprite(name):
    if SPRITES.has_key(name):
        return SPRITES[name]
    else:
        a = sprite.Sprite(name)
        SPRITES[name] = a
        return a


SOUNDS = {}
def getSound(name):
    if SOUNDS.has_key(name):
        return SOUNDS[name]
    else:
        a = loadSound(name)
        SOUNDS[name] = a
        return a
