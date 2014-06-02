import pyglet

import os

# Doesn't search recursively.
pyglet.resource.path = ['images', 'sound']
pyglet.resource.reindex()

# XXX: Sort out AVbin and make oggs work
def loadSound(name):
    a = pyglet.resource.media(name + ".wav", streaming=False)
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
    # Pyglet already caches images
    img = pyglet.resource.image(name + '.png')
    # Set the point the image gets rotated around
    # to the image's center.
    img.anchor_x = int(img.width // 2)
    img.anchor_y = int(img.height // 2)
    return img



def getSprite(name):
    img = getImage(name)
    return pyglet.sprite.Sprite(img)


SOUNDS = {}
def getSound(name):
    if SOUNDS.has_key(name):
        return SOUNDS[name]
    else:
        a = loadSound(name)
        SOUNDS[name] = a
        return a
