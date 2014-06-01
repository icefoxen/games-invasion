# I wonder if this already exists?
# Meh, dependancies.  Don't care

import math

ZERO = (0.0, 0.0)
X = (1.0, 0.0)
Y = (0.0, 1.0)
PIOVER2 = math.pi / 2
PIOVER4 = math.pi / 4

def new(x, y): return (float(x), float(y))

def add(v1, v2):
    r1 = v1[0] + v2[0]
    r2 = v1[1] + v2[1]
    return (r1, r2)

def sub(v1, v2):
    r1 = v1[0] - v2[0]
    r2 = v1[1] - v2[1]
    return (r1, r2)

def mul(v1, s):
    r1 = v1[0] * s
    r2 = v1[1] * s
    return (r1, r2)

# div-by-zero?
# Eh, will just throw an exception if that happens.
def div(v1, s):
    r1 = v1[0] / s
    r2 = v1[1] / s
    return (r1, r2)

def magSquared(v):
    return v[0] * v[0] + v[1] * v[1]

def mag(v):
    return math.sqrt(magSquared(v))

def unit(v):
    m = mag(v)
    return div(v, m)

def dot(v1, v2):
    return (v1[0] * v2[0]) + (v1[1] * v2[1])

# Angle is in radians,
# increasing counterclockwise, 
# with the origin facing right.
# NO MORE
# Angle is in degrees, increasing clockwise,
# with the origin facing up
def fromAngle(angle):
    rads = math.radians(angle)
    x = math.sin(rads)
    y = math.cos(rads)
    return new(x, y)

def toAngle(v):
    return -math.degrees(math.atan2(v[1], v[0]))+90

def toInt(v):
    return (int(v[0]), int(v[1]))

# Constrains the vector's magnitude to the value given.
def cap(v, magnitude):
    m = magnitude * magnitude
    m2 = magSquared(v)
    if m2 > m:
        m = mag(v)
        v2 = unit(v)
        v2 = mul(v2, magnitude)
        return v2
    else:
        return v

# Returns true if the points v1 and v2 are within dist units of each other
def within(v1, v2, dist):
    d = sub(v1, v2)
    return magSquared(d) < (dist * dist)

# Returns a vector perpendicular to the given one
# In no particular direction.
def perpendicular(v):
    return new(v[1], v[0] * -1)


# Returns angle between two vectors.
# Fails for zero vectors, but we shouldn't have those anyway.
def angleBetween((ax, ay), (bx, by)):
    return math.degrees(math.atan2(by, bx) - math.atan2(ay, ax))

# Returns true if the two vectors are within the given number
# of degrees from each other
def angleWithin(va, vb, angle):
    angle /= 2
    ang = angleBetween(va, vb)
    return (ang <= angle) or ((360 - ang) <= angle)

def rotate(v, angle):
    rads = math.radians(angle)
    ca = math.cos(rads)
    sa = math.sin(rads)
    x = v[0] * ca - v[1] * sa
    y = v[0] * sa + v[1] * ca
    return new(x, y)

def invert(v):
    return mul(v, -1.0)

