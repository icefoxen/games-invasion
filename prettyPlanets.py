import pyglet

import random

import resource

def makePrettyPlanet():
    base = resource.getImage('planet2')
    pixs = base.get_image_data()
    #print "Image format:", pixs.format
    pixdata = pixs.get_data('RGBA', pixs.width * 4)
    #print "Pixdata type:", type(pixdata)

    build = []

    for y in range(pixs.height):
        for x in range(pixs.width):
            build.append(pixdata[(y*pixs.width + x) * 4 + 0])
            build.append(pixdata[(y*pixs.width + x) * 4 + 1])
            build.append(pixdata[(y*pixs.width + x) * 4 + 2])
            build.append(pixdata[(y*pixs.width + x) * 4 + 3])
            continue
            # R
            if random.random() < 0.2:
                build.append(chr(int(random.random() * 255)))
            else:
                build.append(pixdata[(y*pixs.width + x) * 4 + 0])
            # G
            if random.random() < 0.2:
                build.append(chr(int(random.random() * 255)))
            else:
                build.append(pixdata[(y*pixs.width + x) * 4 + 1])
            # B
            if random.random() < 0.2:
                build.append(chr(int(random.random() * 255)))
            else:
                build.append(pixdata[(y*pixs.width + x) * 4 + 2])
            # A
            build.append(chr(255))

    imagedata = ''.join(build)
    #print "FOO:", len(pixdata), len(imagedata)
    pixs.set_data('RGBA', pixs.width * 4, imagedata)
    tex = pixs.get_texture()
    tex.anchor_x = int(tex.width // 2)
    tex.anchor_y = int(tex.height // 2)
                

    return pyglet.sprite.Sprite(tex)
