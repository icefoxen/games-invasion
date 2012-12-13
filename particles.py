
import pygame
from pygame.locals import *

import random
import math

import resource
import vec

TWOPI = math.pi * 2

class Particle(object):
    def __init__(s, loc, vel, image, life):
        s.loc = loc
        s.vel = vel
        s.img = resource.getImage(image)
        s.life = life
        s.alive = True

    def update(s, dt):
        #s.loc = vec.mul(vec.add(s.loc, s.vel), dt)
        s.loc = vec.add(s.loc, vec.mul(s.vel, dt))
        s.life -= dt
        if s.life < 0:
            s.alive = False

    def draw(s, surf, gs):
        sloc = gs.screenCoords(s.loc)
        surf.blit(s.img, sloc)
        

# It'd look better if we had actual fire puffs that expanded as they went
# and maybe had some alpha.  But this ain't OpenGL!  We don't have no
# hardware acceleration!  This is SOFTWARE, bitches!
class DriveParticle(Particle):
    def __init__(s, loc, vel):
        images = ["drivepart1", "drivepart2", "drivepart3"]
        img = images[random.randrange(len(images))]
        lifeVariance = random.random() + 1.0
        Particle.__init__(s, loc, vel, img, lifeVariance)

class BloodSplat(Particle):
    def __init__(s, loc, vel):
        Particle.__init__(s, loc, vel, "blood", 0.3)

class AlienBloodSplat(Particle):
    def __init__(s, loc, vel):
        Particle.__init__(s, loc, vel, "greenblood", 0.3)

class HitChip(Particle):
    def __init__(s, loc, vel):
        Particle.__init__(s, loc, vel, "buildingchip", 0.3)

class WarpSpark(Particle):
    def __init__(s, loc, vel):
        Particle.__init__(s, loc, vel, "warpspark", 1.0)


# Spits out a stream of particles.
# Good for engine trails, blood splatters, smoke...
class ParticlePlume(object):
    def __init__(s, particle, speed=1.0, angle=1.0, count=20, interval=0.1):
        s.particleType = particle
        s.speed = speed
        s.angle = angle
        # Emits n particles every x seconds.
        s.count = count
        s.interval = interval
        s.timer = 0.0


    def emit(s, gs, dt, loc, facing, vel=vec.ZERO):
        s.timer += dt
        while s.timer > s.interval:
            s.timer -= s.interval
            for i in range(s.count):
                variance = + (s.angle * random.random()) - (s.angle / 2.0)
                angle = facing + variance
                v = vec.mul(vec.fromAngle(angle), s.speed)
                v = vec.add(vel, v)
                part = s.particleType(loc, v)
                gs.addParticle(part)
            

# A one-shot spray of particles in all directions...
def spray(gs, particle, loc, vel, count):
    for i in range(count):
        velscale = random.gauss(vel, (vel / 3.0))
        direction = random.random() * TWOPI
        velvec = vec.mul(vec.fromAngle(direction), velscale)
        p = particle(loc, velvec)
        gs.addParticle(p)
