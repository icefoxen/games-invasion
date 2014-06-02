
import pyglet
import pyglet.window.key as keys

import math
import random

import particles
import prettyPlanets
import resource
import vec

TWOPI = math.pi * 2
PIOVERTWO = math.pi / 2
PIOVERFOUR = math.pi / 4

def randomAngle():
    return random.random() * 360

# XXX: Make this work
class Background(object):
    def __init__(s):
        starstep = 100
        s.stars = []        
        #for i in range(starstep):
        #    for j in range(starstep):
        s.starsprite = resource.getSprite('planet')
        s.starsprite.scale = 0.1
        
    # XXX: Only draw things in screen view
    # Seems that pygame handles that for us...
    # Layers?  Ambient terrain (big stars, nebula, etc)?
    # Really, having separate objects is the punk's way...
    # We either want a tiled background, or a function we can plug
    # coordinates into that spits out a list of X appropriate stars
    # for the area...
    # XXX: Still, this needs to be made better.
    def draw(s, gs):
        starstep = 100
        # This would be nicer if it worked.  But, screw it for now.  More important things.
        # nearx = int(gs.camerax - (gs.camerax % starstep)) - (gs.screenW / 2) + starstep
        # farx = nearx + gs.screenW
        # neary = int(gs.cameray - (gs.cameray % starstep)) - (gs.screenH / 2) + starstep
        # fary = nearx + gs.screenH
        # for i in range(nearx, farx, starstep):
        #     for j in range(neary, fary, starstep):
        #         dist = vec.mag(vec.new(i,j))
        #         relativeDist = dist / gs.universeSize
        #         brightness = 255 - min(255, int(255 * relativeDist))
        #         sc = gs.screenCoords(vec.new(i, j))
        #         pygame.draw.circle(surf, pygame.Color(brightness,brightness,brightness), sc, 2)


        xoff = int(gs.camerax) % starstep
        yoff = int(gs.cameray) % starstep
        sprite = resource.getSprite('warpspark')
        for i in range(0, gs.screenW + starstep, starstep):
            for j in range(0, gs.screenH + starstep, starstep):
                dist = vec.mag(vec.new(gs.camerax, gs.cameray))
                relativeDist = dist / gs.universeSize
                brightness = 255 - min(255, int(255 * relativeDist))
                sprite.x = i-xoff
                sprite.y = j-yoff
                sprite.draw()
                #XXX: pygame.draw.circle(surf, pygame.Color(brightness,brightness,brightness), (i-xoff,j-yoff), 2)

# XXX: How do we handle the edges of the universe?
# Just have things bounce off of them.
class GameState(object):
    def __init__(s, screenw, screenh):
        s.planets = []
        s.camerax = 0.0
        s.cameray = 0.0
        s.screenW = screenw
        s.screenH = screenh
        s.gameRunning = True
        s.background = Background()
        s.universeSize = 2000

        s.particles = []

        #s.player = SteerablePlanet()
        s.player = Invader()
        s.initUniverse()
        
        

    def addRandomPlanet(s):
        # 0) Generate planet stats: Radius, color, etc
        # 1) Is planet inhabited?
        # 2) How densely inhabited is planet? (Should be weighted by radius)
        # 3) How heavily defended is planet? (Should be weighted by pop density)
        # 4) Does planet have an engine?
        sz = s.universeSize
        x = random.randrange(-sz, sz)
        y = random.randrange(-sz, sz)
        vx = random.random()
        vy = random.random()

        #facing = random.random() * TWOPI
        facing = 0.0
        # Planet has an engine?
        #if random.random() > 0.9:
        #    r = random.randrange(100, 150)
        #    p = SteerablePlanet(vec.new(x, y), r)
        #    p.addBuilding('engine', 0.0)
        #else:
        #    r = random.randrange(50, 200)
        #    p = Planet(vec.new(x, y), r)
        r = random.randrange(50, 200)
        p = Planet(vec.new(x, y), r)

        theta = randomAngle()
        r = 350
        p.loc = vec.new(math.cos(theta) * r, math.sin(theta) * r)

        p.vel = vec.new(vx, vy)
        p.facing = facing

        # Planet is inhabited?
        if random.random() > 0.3:
            #print("Planet is inhabited")
            r = random.random()
            for i in range(random.randrange(3) + 2):
                #loc = random.random() * TWOPI
                #b = Building('small')
                p.addBuilding('small')
                p.addCivvie()
            if r > 0.5:
                #print("Medium inhabited")
                p.addSoldier()
                for i in range(random.randrange(3) + 2):
                    p.addBuilding('medium')
                    p.addCivvie()
            if r > 0.8:
                #print("Densely inhabited")
                p.addSoldier()
                for i in range(random.randrange(3) + 2):
                    p.addBuilding('large')
                    p.addCivvie()

        # Planet is defended?
        r = random.random()
        if r > 0.3:
            # Lightly defended
            for i in range(random.randrange(3)):
                p.addSoldier()
        if r > 0.7:
            # Medium defended
            for i in range(random.randrange(3) + 1):
                p.addSoldier()
        if r > 0.9:
            # Heavily defended
            for i in range(random.randrange(3) + 2):
                p.addSoldier()

        #x = 300
        #y = 0

        s.planets.append(p)

    def initUniverse(s):
        for i in range(4):
            s.addRandomPlanet()
        p = SteerablePlanet(vec.ZERO, 80.0)
        # Invaders are red!
        p.color = 0 # XXX pygame.Color(200, 0, 0)
        p.addSurfFeature(s.player, 0.1)
        p.addBuilding('engine', 0.0)
        #s.planets[0].parent = p
        #s.planets[0].parentVec = vec.new(150, 0)
        s.planets.append(p)

    def update(s, dt):
        #print("# of particles: %d" % len(s.particles))
        for i in s.planets:
            i.update(s, dt)
            for f in i.surfFeatures:
                f.update(s, dt)
                if not f.alive:
                    f.die(s)
                    i.surfFeatures.remove(f)
            #if (s.player.parent != i) and \
            #        (s.player.parent.canCapture(s.player.parent.facing, 1000, i)):
            #    print("Can capture planet!")

        for p in s.particles:
            p.update(dt)
            if not p.alive:
                s.particles.remove(p)

        s.player.update(s, dt)
        s.camerax = s.player.parent.loc[0]
        s.cameray = s.player.parent.loc[1]

        if not s.player.alive:
            s.gameRunning = False

    # XXX: This is dumb, you should be using vector math.
    def screenCoords(s, loc):
        screenx = int(loc[0] - s.camerax) + (s.screenW / 2)
        screeny = int(loc[1] - s.cameray) + (s.screenH / 2)
        return (screenx, screeny)

    def addParticle(s, part):
        s.particles.append(part)

        


# Should facing be a unit vector???
class PhysicsObj(object):
    def __init__(s, loc, mass=1.0, facing=0):
        #GameObj.__init__(s)
        s.loc = loc
        s.mass = mass
        s.facing = facing
        # Velocity units are pixels per second
        s.vel = vec.new(0.0, 0.0)
        # Rotational velocity units are radians per second
        #s.rvel = (random.random() * 0.3) - 0.15
        s.rvel = 0.0
        # Moment of inertia
        s.moment = 1.0

    def updatePhysics(s, dt):
        s.loc = vec.add(s.loc, vec.mul(s.vel, dt))
        s.facing = s.facing + (s.rvel * dt)
        s.facing = s.facing % 360

    # XXX: Enforce max speed and max rotational speed!
    def applyForce(s, force):
        dv = vec.div(force, s.mass)
        s.vel = vec.add(s.vel, dv)

    def applyRforce(s, force):
        dv = force / s.moment
        s.rvel += dv


    def update(s, gs, dt):
        #GameObj.update(s, gs, dt)
        s.updatePhysics(dt)

class Planet(PhysicsObj):
    def __init__(s, loc, radius):
        PhysicsObj.__init__(s, loc, 1.0)
        # Density for planets is pretty constant, I guess...
        # These numbers should also be pretty low, probably...
        s.radius = radius
        s.mass = radius
        s.moment = radius
        r = random.randrange(64, 255)
        g = random.randrange(64, 255)
        b = random.randrange(64, 255)
        s.color = 0 # XXX: pygame.Color(r, g, b)

        s.parent = None
        s.parentVec = vec.ZERO
        s.capturedParentFacing = 0.0
        s.capturedFacing = 0.0
        s.children = []
        s.surfFeatures = []
        s.sprite = s._getPlanetSprite()
        scale = radius / 64.0
        s.sprite.scale = scale
        s.captureSprite = None

    def _getPlanetSprite(self):
        return prettyPlanets.makePrettyPlanet()


    def addSurfFeature(s, feat, loc):
        s.surfFeatures.append(feat)
        feat.setParent(s)
        feat.loc = loc

    def addBuilding(s, typ, loc=None):
        if loc == None:
            loc = randomAngle()
        b = Building(typ)
        s.addSurfFeature(b, loc)

    def addSoldier(s, loc=None):
        if loc == None:
            loc = randomAngle()
        b = Soldier()
        s.addSurfFeature(b, loc)

    def addCivvie(s, loc=None):
        if loc == None:
            loc = randomAngle()
        b = Civvie()
        s.addSurfFeature(b, loc)

    def draw(s, gs):
        sx, sy = gs.screenCoords(s.loc)
        s.sprite.x = sx
        s.sprite.y = sy
        s.sprite.rotation = s.facing
        s.sprite.draw()
        if s.parent != None:
            #parentSloc = gs.screenCoords(s.parent.loc)
            vecToParent = vec.sub(s.parent.loc, s.loc)
            angle = vec.toAngle(vecToParent)
            centerPointVec = vec.div(vecToParent, 2)
            actualVec = vec.add(s.loc, centerPointVec)
            s.captureSprite.position = gs.screenCoords(actualVec)
            s.captureSprite.rotation = angle
            s.captureSprite.draw()
    
    
    # A bit of an ugly hack, buuuuut...
    # XXX: Should add children's mass and moment of inertia to its own,
    # at least partially!
    def update(s, gs, dt):
        if s.parent == None:
            PhysicsObj.update(s, gs, dt)
        else:
            #print("parent offset: {0}, parent direction {1}, parent distance {2}, parent facing {3}".format(s.parentVec, vec.toAngle(p), vec.mag(p), s.parent.facing))
             # To figure out the current facing we must know what our parent's facing is,
             # where we were facing when captured, and where the parent was facing when captured.
            s.facing = s.capturedFacing + (s.parent.facing - s.capturedParentFacing)

            rotation = s.parent.facing - s.capturedParentFacing +180
            p = vec.rotate(s.parentVec, -rotation)
            # THAT FUCKING SIMPLE AAAAAAAAAAH
            relativePosition = vec.add(s.parent.loc, p)
            s.loc = relativePosition

            
    def isParent(s, planet):
        """Returns true if the given planet is a parent of the current one or
        any in the tree above it.
        Useful for avoiding loops in the planet parentage tree."""
        if s.parent != None:
            return s.parent == planet or s.parent.isParent(planet)
        else:
            return False


    # Okay... so this function will attempt to snag another nearby planet.
    # It just checks if we're near enough to it and if we are more or less facing it.
    # XXX: Require a low relative velocity, as well??  Possibly!
    def canCapture(s, point, distance, targetPlanet):
        if s.isParent(targetPlanet):
            #print "Nope, is parent"
            return False
        if targetPlanet.parent != None:
            #print "Nope, has parent"
            return False
        if targetPlanet == s:
            #print "Nope, self"
            return False
        if s in targetPlanet.children:
            #print "Nope, is a child already"
            return False

        vecBetweenPlanets = vec.sub(targetPlanet.loc, s.loc)
        # Adjust distance to measure from surface to surface, not center
        # to center
        distance += s.radius + targetPlanet.radius
        if vec.magSquared(vecBetweenPlanets) > (distance*distance):
            #print "Nope, out of range"
            return False
        
        # Okay we are close enough to an eligible planet, are we facing it?
        angleBetweenPlanets = vec.toAngle(vecBetweenPlanets)
        # Urrrrrg I hate this, -180 to 180 and 0-360 behave differently and both are
        # awful in different situations so neither one is really correct.
        point = (point + 360) % 360
        angleBetweenPlanets = (angleBetweenPlanets + 360) % 360
        print "Point and angle:", point, angleBetweenPlanets
        if abs(angleBetweenPlanets - point) < 10:
            #print "Yep!"
            return True

        #print "Nope, angle too great", angleBetweenPlanets, point, abs(angleBetweenPlanets - point)
        return False



        vecBetweenPlanets = vec.sub(targetPlanet.loc, s.loc)
        vecBPU = vec.unit(vecBetweenPlanets)
        vecToPlanetEdge = vec.mul(vec.perpendicular(vecBPU), targetPlanet.radius)
        #print("Vec between planets: {0}, vec to planet edge: {1}".format(vecBPU, vec.unit(vecToPlanetEdge)))
        angularSize = vec.angleBetween(vecBetweenPlanets, vec.add(vecBetweenPlanets, vecToPlanetEdge))
        vecToPoint = vec.mul(vec.fromAngle(point), s.radius)
        angularDistance = vec.angleBetween(vecBetweenPlanets, vecToPoint)
        #print("Angular size: {0}, angular distance: {1}".format(angularSize, angularDistance))
        if angularDistance > abs(angularSize):
            return False
        else:
            # Check distance between planets surfaces
            distance = distance + (s.radius + targetPlanet.radius)
            # Can't capture a planet if you're overlapping it
            # XXX: Doesn't seem to work, but...
            if distance < 0:
                return False
            return vec.within(s.loc, targetPlanet.loc, distance)

    def genCaptureImage(s):
        """Builds a line sprite of the right length to go to the capturing planet."""
        # Some paranoid error checking
        if not s.parent:
            raise Exception("Tried to generate capture image with nonexistant parent!")
        vecToParent = vec.sub(s.parent.loc, s.loc)
        distanceToParent = vec.mag(vecToParent)
        # It appears that we can blit image_data (software image data
        # in main memory) to a texture (hardware image data on the GPU)
        # but not any other way.
        ropeImage = resource.getImage('line2').get_image_data()
        img = pyglet.image.create(ropeImage.width, int(distanceToParent)).get_texture()
        img.anchor_x = int(img.width // 2)
        img.anchor_y = int(img.height // 2)

        # Now we have the image, we fill it up with the
        # capture-rope images.
        for i in range(0, int(distanceToParent), ropeImage.height):
            #print 'foo', i, img.height, ropeImage.height
            img.blit_into(ropeImage, 0, i, 0)

        s.captureSprite = pyglet.sprite.Sprite(img)

    def capture(s, victimPlanet):
        # This vector points from self to the victim planet
        distance = vec.sub(s.loc, victimPlanet.loc)
        victimPlanet.parentVec = distance
        victimPlanet.parent = s
        victimPlanet.capturedFacing = victimPlanet.facing
        victimPlanet.capturedParentFacing = s.facing
        s.children.append(victimPlanet)
        victimPlanet.genCaptureImage()
        

    def uncapture(s, victimPlanet):
        if victimPlanet in s.children:
            s.children.remove(victimPlanet)
            victimPlanet.parent = None
            victimPlanet.captureSprite = None

        



class SteerablePlanet(Planet):
    def __init__(s, loc, radius):
        Planet.__init__(s, loc, radius)
        s.vel = vec.ZERO
        s.rvel = 0.0
        
        s.thrusting = False
        s.turning = 0
        s.thrustForce = 2000.0
        s.turnForce = 2000.0
        # Invaders are red!
        #s.color = pygame.Color(200, 0, 0)

        #f = SurfFeature()
        #s.addSurfFeature(f, 0.5)

        s.controller = None
        s.controlPoint = 0.0

        s.driveEmitter = particles.ParticlePlume(particles.DriveParticle, speed=80.0, angle=30.0, count=3, interval=0.05)
        s.engineSound = resource.getSound("engine")

    def clearInput(s):
        s.thrusting = False
        s.turning = 0.0

    def on_key_press(s, gs, key):
        if key == keys.UP:
            s.thrusting = True
            s.engineSound.play() # loops=-1, fade_ms=200)
            
        elif key == keys.LEFT:
            s.turning = -1.0
        elif key == keys.RIGHT:
            s.turning = 1.0

    def on_key_release(s, gs, key):
        if key == keys.UP:
            s.thrusting = False
            # XXX
            # s.engineSound.fadeout(500)
        elif key == keys.LEFT:
            s.turning = 0
        elif key == keys.RIGHT:
            s.turning = 0        


    def update(s, gs, dt):
        #print(s.vel)
        if s.thrusting:
            force = s.thrustForce * dt
            facing = vec.fromAngle(s.facing + 180)
            f = vec.mul(facing, force)
            s.applyForce(f)

            offset = vec.fromAngle(s.facing)
            offset = vec.mul(offset, s.radius)
            loc = vec.add(s.loc, offset)
#            v = vec.invert(s.vel)
            s.driveEmitter.emit(gs, dt, loc, s.facing, vel=s.vel)

        # Turning should be either 0, -1 or +1
        if s.turning != 0:
            force = s.turnForce * dt * s.turning
            s.applyRforce(force)

        Planet.update(s, gs, dt)

# A feature on the surface of a planet
# So... people, buildings, etc.
# Notable mainly in that it keeps its location relative to the parent planet...
# Parent must be a planet, at the moment.
# Thus captured planets could count as these?  Hrm.
class SurfFeature(object):
    def __init__(s):
        #GameObj.__init__(s)
        s.parent = None
        s.loc = 0.0
        s.size = 2.0
        s.hits = 10
        s.alive = True
        s.sprite = resource.getSprite("test")
        s.radius = 0.0
        s.hitCooldown = 0.0
        s.hitCooldownTotal = 0.5
        s.damageParticle = particles.HitChip
        s.hitSound = resource.getSound("buildinghit")
        s.dieSound = resource.getSound("buildingdie")

    def die(s, gs):
        s.dieSound.play()

    def setParent(s, parent):
        if parent != None:
            s.parent = parent
            s.radius = parent.radius + 1.0

    def draw(s, gs):
        rot = s.parent.facing + s.loc
        totalAngle = vec.fromAngle(rot)
        offsetVec = vec.mul(totalAngle, s.radius)
        location = vec.add(s.parent.loc, offsetVec)
        (scx, scy) = gs.screenCoords(location)
        #print "rot: %s, totalAngle: %s, offsetVec: %s, location: %s, sc: %s" % (rot, totalAngle, offsetVec, location, (scx, scy))
        # Add a slight offset to center the image rather than drawing
        # it from the lower-left corner...
        # Also add oregano.
        s.sprite.rotation = s.loc + s.parent.facing
        #print s.sprite.rotation, s.loc, s.parent.facing
        s.sprite.position = (scx, scy)
        s.sprite.draw()


    def move(s, amount):
        s.loc += amount

    def sprayParticles(s, gs, particle, speed, count):
        offset = vec.fromAngle(s.loc + s.parent.facing)
        offset = vec.mul(offset, s.radius)
        loc = vec.add(s.parent.loc, offset)
        particles.spray(gs, particle, loc, speed, count)

    def damage(s, gs, amount):
        if s.hitCooldown < 0.0:
            s.hitSound.play()
            s.hits -= amount
            s.hitCooldown = s.hitCooldownTotal
            s.sprayParticles(gs, s.damageParticle, 100.0, 30)



    def update(s, gs, dt):
        if s.hits < 1:
            s.alive = False

        s.hitCooldown -= dt
        s.loc = s.loc % 360

    # XXX: This has the same range problem as bullets
    # XXX: This also doesn't really handle vertical size correctly.
    def isTouching(s, other):
        lvec = vec.fromAngle(s.loc)
        olvec = vec.fromAngle(other.loc)
        return (abs(vec.angleBetween(lvec, olvec)) < (s.size + other.size)) \
            and abs(s.radius - other.radius) < ((s.size + other.size) * 10)
        # s.loc = s.loc % TWOPI
        # other.loc = other.loc % TWOPI
        # distance = abs(s.loc - other.loc)
        # return (s.size + other.size) < distance


BUILDING = {
    # Building name : (building sprite, size, hits)
    'small' : ("smallbuilding", 8.5, 10),
    'medium' : ("mediumbuilding", 12.0, 20),
    'large' : ("largebuilding", 12.0, 30),
    # Engines aren't invulnerable, but at the moment they might as well be.
    'engine' : ("engine", 12.0, 30000000000000),
}

class Building(SurfFeature):
    def __init__(s, buildingType):
        SurfFeature.__init__(s)
        (img, size, hits) = BUILDING[buildingType]
        s.size = size
        s.hits = hits
        s.sprite = resource.getSprite(img)
        

# Duuuuuuuuude.
# (Any generic guy-type thing)
class Dude(SurfFeature):
    def __init__(s):
        SurfFeature.__init__(s)
        s.speed = 15.0
        s.moving = 0
        s.controlling = False
        s.captureRange = 500
        s.transportCooldownTotal = 2.0
        s.transportCooldown = 0.0
        s.facing = 1
        s.attackCooldownTotal = 1.0
        s.attackCooldown = 0.0

        s.jumpCooldownTotal = 1.0
        s.jumpCooldown = 0.0
        s.damageParticle = particles.BloodSplat
        s.hitSound = resource.getSound("enemyhit")
        s.dieSound = resource.getSound("enemydie")
        s.attackSound = resource.getSound("shot")
        s.teleportSound = resource.getSound("teleport")
        s.jumpSound = resource.getSound("jump")

    def clearInput(s):
        s.moving = 0

    # The locations here are a little squirrelly still, I think...
    def startControl(s):
        if s.parent.__class__ != SteerablePlanet:
            return
        locvec = vec.fromAngle(s.loc)
        controlpointvec = vec.fromAngle(s.parent.controlPoint)
        diff = vec.angleBetween(locvec, controlpointvec)
        if abs(diff) < 10.0:
            #print("Took control")
            s.controlling = True
            s.loc = s.parent.controlPoint
            s.clearInput()
        else:
            pass
            #print("Did not take control: Loc = {0}, control point = {1}".format(s.loc, s.parent.controlPoint))

    def endControl(s):
        s.controlling = False
        s.parent.clearInput()

    def on_key_press(s, gs, key):
        if key == keys.SPACE:
            if not s.controlling:
                s.startControl()
            else:
                s.endControl()
        elif s.controlling:
            s.parent.on_key_press(gs, key)
        else:
            if key == keys.LEFT:
                s.facing = -1
                s.moving = -1
            elif key == keys.RIGHT:
                s.facing = 1
                s.moving = 1
            elif key == keys.X:
                # Try capture some nearby planet...
                #print("Trying capture...")
                for p in gs.planets:
                    facingpoint = (s.parent.facing + s.loc) % 360
                    #print("Trying to capture {0} at facing {1}".format(p, facingpoint))
                    # XXX: Make it only capture the closest planet, dammit!
                    # XXX: Ideally it will also go off the distance between the planet
                    # surfaces, not the centers  This needs to happen!
                    if s.parent.canCapture(facingpoint, s.captureRange, p):
                        print("Captured, facing {0}!".format(facingpoint))
                        s.parent.capture(p)
                        sound = resource.getSound("capture")
                        sound.play()
                        break
            elif key == keys.Z:
                # Try uncapture
                # XXX: At the moment we can't uncapture from the child side... hmm.
                # XXX: At the moment also, if there are multiple planets
                # captured close to each other, it essentially releases
                # one at random rather than doing the one closest to 
                # where you're standing.
                for p in s.parent.children:
                    # This is a little fucked up but should work...
                    facingpoint = (s.parent.facing + s.loc) % 360
                    facingvec = vec.fromAngle(facingpoint)
                    offset = vec.sub(p.loc, s.parent.loc)
                    diff = vec.angleBetween(facingvec, offset)

                    if abs(diff) < 0.2:
                        #print("Uncapturing")
                        s.parent.uncapture(p)
                        sound = resource.getSound("uncapture")
                        sound.play()
                        break

            elif key == keys.C:
                if s.attackCooldown < 0.0:
                    s.attack(gs)
                    s.attackCooldown = s.attackCooldownTotal
                    s.attackSound.play()
                

            elif key == keys.UP:
                # Transport to captured planet.
                teleportAngle = 10.0
                for p in s.parent.children:
                    facingpoint = (s.parent.facing + s.loc) % 360
                    facingvec = vec.fromAngle(facingpoint)
                    offset = vec.sub(p.loc, s.parent.loc)
                    diff = vec.angleBetween(facingvec, offset)

                    if abs(diff) < teleportAngle and s.transportCooldown <= 0.0:
                        s.sprayParticles(gs, particles.WarpSpark, 50, 30)
                        facingdiff = s.parent.facing - p.facing
                        s.loc += facingdiff + 180
                        s.setParent(p)
                        s.transportCooldown = s.transportCooldownTotal
                        s.sprayParticles(gs, particles.WarpSpark, 50, 30)
                        s.teleportSound.play()
                        return
                
                # Oooor, if this planet is captured, you can go back to the parent
                if s.parent.parent != None:
                    p = s.parent.parent
                    facingpoint = (s.parent.facing + s.loc) % 360
                    facingvec = vec.fromAngle(facingpoint)
                    offset = vec.sub(p.loc, s.parent.loc)
                    diff = vec.angleBetween(facingvec, offset)
                    if abs(diff) < teleportAngle and s.transportCooldown <= 0.0:
                        s.sprayParticles(gs, particles.WarpSpark, 50, 30)
                        facingdiff = s.parent.facing - p.facing
                        s.loc += facingdiff + 180
                        s.setParent(p)
                        s.transportCooldown = s.transportCooldownTotal
                        s.sprayParticles(gs, particles.WarpSpark, 50, 30)
                        s.teleportSound.play()
                        return

                # If we've gotten this far, then you're not sitting on a connection,
                # So jump!
                if s.jumpCooldown < 0:
                    s.jump()
                    s.jumpSound.play()
                

                

    def on_key_release(s, gs, key):
        if s.controlling:
            s.parent.on_key_release(gs, key)
        else:
            if key == keys.LEFT or key == keys.RIGHT:
                s.moving = 0
            
    def update(s, gs, dt):
        SurfFeature.update(s, gs, dt)
        # Floating point wraparound?  Meh
        s.transportCooldown = max(s.transportCooldown - dt, 0)
        s.move(s.speed * dt * s.moving)
        if s.jumpCooldown > 0.0:
            jump = 50.0 * math.sin(s.jumpCooldown * math.pi)
            s.radius = s.parent.radius + jump
        else:
            s.radius = s.parent.radius
        s.attackCooldown -= dt
        s.jumpCooldown -= dt

    def attack(s, gs):
        print("Raaah!")

    def jump(s):
        s.jumpCooldown = s.jumpCooldownTotal
        #print("Boing!")


class Civvie(Dude):
    def __init__(s):
        Dude.__init__(s)
        s.hits = 10
        s.sprite = resource.getSprite('civvie')
        s.aiCooldownMax = 1.0
        s.aiCooldown = random.random() * s.aiCooldownMax
        s.ai = CivvieAI(s)


    def update(s, gs, dt):
        Dude.update(s, gs, dt)
        s.aiCooldown -= dt
        if s.aiCooldown < 0:
            s.aiCooldown = s.aiCooldownMax
            s.ai.command(gs)



class Soldier(Dude):
    def __init__(s):
        Dude.__init__(s)
        s.hits = 20
        s.sprite = resource.getSprite('soldier')
        s.aiCooldownMax = 1.5
        s.aiCooldown = random.random() * s.aiCooldownMax
        s.ai = SoldierAI(s)
        s.damageParticle = particles.BloodSplat

    # XXX: Location of attacks is squirrelly
    def attack(s, gs):
        b = Bullet(s, s.parent, s.facing)
        loc = s.loc + (s.facing * 0.2)
        s.parent.addSurfFeature(b, loc)

    def update(s, gs, dt):
        Dude.update(s, gs, dt)
        s.aiCooldown -= dt
        if s.aiCooldown < 0:
            s.aiCooldown = s.aiCooldownMax
            s.ai.command(gs)
        


class Invader(Dude):
    def __init__(s):
        Dude.__init__(s)
        s.hits = 50
        s.sprite = resource.getSprite('invader')
        s.damageParticle = particles.AlienBloodSplat
        s.hitSound = resource.getSound("invaderhit")
        s.dieSound = resource.getSound("enemydie")
        s.attackSound = resource.getSound("swing")

    # XXX: Location of attacks is squirrelly
    def attack(s, gs):
        b = Blade(s, s.parent, s.facing)
        loc = s.loc + (s.facing * 0.2)
        s.parent.addSurfFeature(b, loc)

# XXX: Bullets should not hurt NPC's!
class Bullet(SurfFeature):
    def __init__(s, creator, parent, direction=1):
        SurfFeature.__init__(s)
        #s.loc = creator.loc + (direction * 0.2)
        s.direction = direction
        s.speed = 52.0
        s.lifetime = 1.0
        s.setParent(s)
        s.radius += 2.0
        s.creator = creator
        s.size = 1.0
        s.sprite = resource.getSprite("bullet")

    def update(s, gs, dt):
        SurfFeature.update(s, gs, dt)
        s.loc += (s.speed * dt * s.direction)
        s.lifetime -= dt
        things = s.parent.surfFeatures
        if s.lifetime < 0.0:
            s.alive = False
        target = gs.player
        if s.isTouching(target):
            s.alive = False
            target.damage(gs, 1)

    def die(s, gs):
        pass

class Blade(SurfFeature):
    def __init__(s, creator, parent, direction=1):
        SurfFeature.__init__(s)
        #s.loc = creator.loc + (direction * 0.2)
        s.direction = direction
        s.speed = 1.0
        s.lifetime = 0.5
        s.setParent(s)
        s.radius += 2.0
        s.creator = creator
        s.size = 10.0
        s.spriteRight = resource.getSprite("bladeRight")
        s.spriteLeft = resource.getSprite("bladeLeft")
        s.setSprite()

    def setSprite(s):
        if s.direction > 0:
            s.sprite = s.spriteRight
        else:
            s.sprite = s.spriteLeft

    def update(s, gs, dt):
        SurfFeature.update(s, gs, dt)
        s.radius = s.creator.radius
        s.loc = s.creator.loc + (s.direction) * 0.2
        s.lifetime -= dt
        things = s.parent.surfFeatures
        if s.lifetime < 0.0:
            s.alive = False
        
        for t in things:
            if (t != s) and (t != s.creator) and s.isTouching(t):
                #print(t)
                #print("Splutch!")
                t.damage(gs, 5)

    # XXX: Not quite right; need to either fudge angles based on planet size
    # or do a coordinate transform to put it at a fixed pixel offset from the parent.
    def draw(s, gs):
        swingSpeed = 190.0 # Degrees per second
        startingFacing = 90.0
        if s.direction > 0:
            swing = startingFacing + -(s.lifetime * swingSpeed)
        else:
            swing = (s.lifetime * swingSpeed) - startingFacing 
        rot = s.parent.facing + s.loc
        totalAngle = vec.fromAngle(rot)
        offset = vec.mul(totalAngle, s.radius)
        location = vec.add(s.parent.loc, offset)
        s.sprite.position = gs.screenCoords(location)
        #print location
        s.sprite.rotation = rot + swing
        s.sprite.draw()


    def die(s, gs):
        pass


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

AISTATE = enum("Wander", "Attack", "Run")

class AI(object):
    def __init__(s, controlled):
        s.controlled = controlled
        s.state = AISTATE.Wander

    # Wander: Just amble back and forth
    def doWander(s, gs):
        s.controlled.on_key_release(gs, keys.LEFT)
        s.controlled.on_key_release(gs, keys.RIGHT)
        r = random.random()
        if r < 0.3:
            s.controlled.on_key_press(gs, keys.LEFT)
        elif r < 0.6:
            pass
            s.controlled.on_key_press(gs, keys.RIGHT)
        else:
            # Stand where you are.
            pass

    # Attacking: Find an invader on the planet, approach to some range,
    # and open fire while trying to keep distance
    def doAttack(s, gs):
        s.controlled.on_key_release(gs, keys.LEFT)
        s.controlled.on_key_release(gs, keys.RIGHT)
        target = gs.player.loc
        distance = (s.controlled.loc - target) % 360
        desiredDistance = 30
        if distance < desiredDistance:
            # Move further away
            s.controlled.on_key_press(gs, keys.LEFT)
            s.controlled.attack(gs)
            s.controlled.on_key_press(gs, keys.RIGHT)
        elif distance > (360 - desiredDistance):
            # Move further away
            s.controlled.on_key_press(gs, keys.RIGHT)
            s.controlled.attack(gs)
            s.controlled.on_key_press(gs, keys.LEFT)
        elif distance < 180: # and distance > desiredDistance, implicitly
            # Move closer
            s.controlled.on_key_press(gs, keys.LEFT)
            s.controlled.attack(gs)
        elif distance > 180: # and distance < (360 - desiredDistance), implicitly
            # Move closer
            s.controlled.on_key_press(gs, keys.RIGHT)
            s.controlled.attack(gs)
        return

        runfrom = gs.player.loc
        rvloc = vec.fromAngle(runfrom - s.controlled.loc)
        reference = vec.fromAngle(0)
        distance = vec.angleBetween(reference, rvloc)
        print "Distance:", distance
        desiredDistance = 25
        if distance > desiredDistance:
            s.controlled.on_key_press(gs, keys.LEFT)
            s.controlled.attack(gs)
        elif distance > 0:
            s.controlled.on_key_press(gs, keys.RIGHT)
            s.controlled.attack(gs)
            s.controlled.on_key_press(gs, keys.LEFT)
        elif distance < -desiredDistance:
            s.controlled.on_key_press(gs, keys.RIGHT)
            s.controlled.attack(gs)
        elif distance < 0:
            s.controlled.on_key_press(gs, keys.LEFT)
            s.controlled.attack(gs)
            s.controlled.on_key_press(gs, keys.RIGHT)


        

    # Running: Find invader on the planet, move away from them.
    def doRun(s, gs):
        s.controlled.on_key_release(gs, keys.LEFT)
        s.controlled.on_key_release(gs, keys.RIGHT)
        runfrom = gs.player.loc
        distance = (s.controlled.loc - runfrom) % 360
        if distance < 180:
            s.controlled.on_key_press(gs, keys.RIGHT)
        else:
            s.controlled.on_key_press(gs, keys.LEFT)

    def command(s, gs):
        if s.state == AISTATE.Wander:
            s.doWander(gs)
        elif s.state == AISTATE.Attack:
            s.doAttack(gs)
        elif s.state == AISTATE.Run:
            s.doRun(gs)

class SoldierAI(AI):
    def __init__(s, controlled):
        AI.__init__(s, controlled)
        s.state = AISTATE.Wander

    # If no invader on planet, mill about randomly.
    # If invader is near by, approach and shoot.
    # If low on health, try to run.
    def command(s, gs):
        AI.command(s, gs)
        thingsOnPlanet = s.controlled.parent.surfFeatures
        #print gs.player.parent
        #print s.controlled.parent
        if gs.player.parent == s.controlled.parent:
            if s.controlled.hits < 10:
                s.state = AISTATE.Run
            else:
                s.state = AISTATE.Attack
        else:
            s.state = AISTATE.Wander


class CivvieAI(AI):
    def __init__(s, controlled):
        AI.__init__(s, controlled)
        s.state = AISTATE.Wander

    # If no invader on planet, mill about randomly
    # If invader is nearby, has a SMALL chance of shooting
    # Otherwise will run away
    def command(s, gs):
        AI.command(s, gs)
        #print gs.player.parent
        #print s.controlled.parent
        if gs.player.parent == s.controlled.parent:
            if random.random() > 0.95:
                s.state = AISTATE.Attack
            s.state = AISTATE.Run
        else:
            s.state = AISTATE.Wander
