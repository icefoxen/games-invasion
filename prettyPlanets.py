import pyglet

import random

import resource

TESTPALETTE = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255)
]

PALETTE1 = [
    (192, 128, 128),
    (192, 192, 192),
    (255, 255, 255),
    (172, 172, 172),
    (190, 190, 190),
    (134, 134, 134),
    (128,  64,  64),
    ( 64,  64,  64),
]

PALETTE2 = [
    (255 - 192, 128, 128),
    (255 - 192, 192, 192),
    (255 - 255, 255, 255),
    (255 - 172, 172, 172),
    (255 - 190, 190, 190),
    (255 - 134, 134, 134),
    (255 - 128,  64,  64),
    (255 - 64,   64,  64),
]

PALETTE3 = [
    (192, 255 - 128, 128),
    (192, 255 - 192, 192),
    (255, 255 - 255, 255),
    (172, 255 - 172, 172),
    (190, 255 - 190, 190),
    (134, 255 - 134, 134),
    (128, 255 - 64,   64),
    (64,  255 - 64,   64),
]

PALETTE4 = [
    (192, 128, 255 - 128),
    (192, 192, 255 - 192),
    (255, 255, 255 - 255),
    (172, 172, 255 - 172),
    (190, 190, 255 - 190),
    (134, 134, 255 - 134),
    (128,  64, 255 -  64),
    ( 64,  64, 255 -  64),
]



PALETTE5 = [
    (255 - 192, 255 - 128, 128),
    (255 - 192, 255 - 192, 192),
    (255 - 255, 255 - 255, 255),
    (255 - 172, 255 - 172, 172),
    (255 - 190, 255 - 190, 190),
    (255 - 134, 255 - 134, 134),
    (255 - 128, 255 - 64,   64),
    (255 - 64,  255 - 64,   64),
]

PALETTE6 = [
    (255 - 192, 128, 255 - 128),
    (255 - 192, 192, 255 - 192),
    (255 - 255, 255, 255 - 255),
    (255 - 172, 172, 255 - 172),
    (255 - 190, 190, 255 - 190),
    (255 - 134, 134, 255 - 134),
    (255 - 128,  64, 255 -  64),
    (255 -  64,  64, 255 -  64),
]

PALETTE7 = [
    (192, 255 - 128, 255 - 128),
    (192, 255 - 192, 255 - 192),
    (255, 255 - 255, 255 - 255),
    (172, 255 - 172, 255 - 172),
    (190, 255 - 190, 255 - 190),
    (134, 255 - 134, 255 - 134),
    (128, 255 -  64, 255 -  64),
    ( 64, 255 -  64, 255 -  64),
]


PALETTE8 = [
    (255 - 192, 255 - 128, 255 - 128),
    (255 - 192, 255 - 192, 255 - 192),
    (255 - 255, 255 - 255, 255 - 255),
    (255 - 172, 255 - 172, 255 - 172),
    (255 - 190, 255 - 190, 255 - 190),
    (255 - 134, 255 - 134, 255 - 134),
    (255 - 128, 255 -  64, 255 -  64),
    (255 -  64, 255 -  64, 255 -  64),
]

PALETTE0 = [
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
]

PALETTES = [PALETTE1, PALETTE2, PALETTE3, PALETTE4, PALETTE5, PALETTE6, PALETTE7, PALETTE8] 

def randomFromPalette(palette):
    return random.choice(palette)

def _pixelsToTex(imagedata, build):
    #print build
    pixelStr = ''.join(build)
    imagedata.set_data('RGBA', imagedata.width * 4, pixelStr)
    tex = imagedata.get_texture()
    tex.anchor_x = int(tex.width // 2)
    tex.anchor_y = int(tex.height // 2)
    return tex

def fill(image, color):
    imagedata = image.get_image_data()
    pixdata = imagedata.get_data('RGBA', imagedata.width * 4)

    (r, g, b) = color

    build = []

    for y in range(imagedata.height):
        for x in range(imagedata.width):
            a = pixdata[(y*imagedata.width + x) * 4 + 3]
            
            build.append(chr(int(r)))
            build.append(chr(int(g)))
            build.append(chr(int(b)))
            build.append(a)

    return _pixelsToTex(imagedata, build)

def speckle(image, palette, density):
    imagedata = image.get_image_data()
    #print "Image format:", pixs.format
    pixdata = imagedata.get_data('RGBA', imagedata.width * 4)
    #print "Pixdata type:", type(pixdata)

    build = []

    for y in range(imagedata.height):
        for x in range(imagedata.width):
            if random.random() < density:
                (r, g, b) = randomFromPalette(palette)
                a = pixdata[(y*imagedata.width + x) * 4 + 3]

                build.append(chr(int(r)))
                build.append(chr(int(g)))
                build.append(chr(int(b)))
                build.append(chr(a))
                #build.append('MARK1')
            else:
                r = pixdata[(y*imagedata.width + x) * 4 + 0]
                g = pixdata[(y*imagedata.width + x) * 4 + 1]
                b = pixdata[(y*imagedata.width + x) * 4 + 2]
                a = pixdata[(y*imagedata.width + x) * 4 + 3]
                build.append(chr(r))
                build.append(chr(g))
                build.append(chr(b))
                build.append(chr(a))
                #build.append('MARK2')
                
    return _pixelsToTex(imagedata, build)

def randomLine(image, palette, count):
    imagedata = image.get_image_data()
    #pixdata = imagedata.get_data('RGBA', imagedata.width * 4)

    #build = []

    # Hopefully this copies the image...
    tex = image.get_texture()

    for i in range(count):
        (r, g, b) = randomFromPalette(palette)
        startx = random.randint(0, imagedata.width - 1)
        starty = random.randint(0, imagedata.height - 1)

        line = fill(resource.getImage('line'), randomFromPalette(palette))
        line = line.get_image_data()
        scale = (random.random() * 10) + 1

        orientation = random.random() * 360

        tex.blit_into(line, startx, starty, 0)

    return tex
        
        
        

def makePrettyPlanet():
    base = resource.getImage('planet')
    palette = random.choice(PALETTES)
    #return randomLine(base, PALETTE1, 10)
    filled = fill(base, randomFromPalette(palette))
    return speckle(filled, palette, 0.2)
