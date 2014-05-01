#!/usr/bin/env python

import pyglet
import cProfile

import os

from world import *
import resource

def handleInput(gs):
    for e in pygame.event.get():
        if e.type == QUIT:
            gs.gameRunning = False
        elif e.type == KEYDOWN:
            #print("Key down event: %s" % e)
            if e.key == K_ESCAPE:
                gs.gameRunning = False
            else:
                gs.player.handleInputStart(gs, e.key)


        elif e.type == KEYUP:
            #print("Key up event: %s" % e)
            gs.player.handleInputEnd(gs, e.key)


# XXX: Stretch image to fill full screen?  Center images?
def doTitleScreen(window):
    logo = resource.loadImage("logo")
    title = resource.loadImage("title")
    fpsDisplay = pyglet.clock.ClockDisplay()
    @window.event
    def on_draw():
        window.clear()
        logo.blit(0,0)
        fpsDisplay.draw()
        

    #surf.fill(pygame.Color(0, 0, 0))
    #surf.blit(logo, (0, 0))
    #pygame.display.flip()
    #pygame.time.wait(2000)

    #surf.fill(pygame.Color(0, 0, 0))
    #surf.blit(title, (0, 0))
    #pygame.display.flip()
    #pygame.event.clear()
    #while True:
    #    for e in pygame.event.get():
    #        if e.type == KEYDOWN:
    #            return

def doGameOver(window):
    gameover = resource.loadImage("gameover")
    window.clear()
    gameover.blit(0,0)
    def doClose(dt):
        window.close()
    pyglet.clock.schedule_once(doClose, 2000)


def mainloop(screenw, screenh):
    window = pyglet.window.Window(width=screenw, height=screenh)
    window.set_vsync(False)
    # XXX: The animation state here is a little wibbly, work on it.
    #doTitleScreen(window)

    gs = GameState(screenw, screenh)
    fpsDisplay = pyglet.clock.ClockDisplay()

    @window.event
    def on_draw():
        window.clear()
        gs.background.draw(window, gs)
        gs.player.draw(window, gs)
        for p in gs.particles:
            p.draw(window, gs)
        for p in gs.planets:
            p.draw(window, gs)
            for f in p.surfFeatures:
                f.draw(window, gs)
                
        fpsDisplay.draw()

    def updateGame(dt):
        gs.update(dt)
        if not gs.player.alive:
            doGameOver(window)
    
    # Game physics get updated at 30FPS
    pyglet.clock.schedule_interval(updateGame, 1/30.0)
    
    pyglet.app.run()


#    statText = "X: {0:5.2f}  Y: {1:5.2f}  Velocity: ({2:5.2f}, {3:5.2f})  Hits: {4}".format(\
#        gs.camerax, gs.cameray, gs.player.parent.vel[0], gs.player.parent.vel[1], gs.player.hits)
#    display = font.render(statText, True, pygame.Color(255, 255, 255), pygame.Color(0,0,0))

    


def main():
    # TODO: Choose resolution
    mainloop(800, 600)
    #cProfile.run('mainloop(800, 600)')

    # Called when interpreter exits anyway
    #pygame.quit()


if __name__ == '__main__':
    main()
