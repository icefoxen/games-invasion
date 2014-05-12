#!/usr/bin/env python

import pyglet
import pyglet.window.key
import cProfile

import os

from world import *
import resource

# Okay, so this pushes two sets of event handlers onto the
# event stack, which displays the splash and title screens.
# With each of them, it also pushes an event handler that
# pops the event stack when a key is pressed.
# This is in contrast to the more straightforward state of
# pushing the game's event handling atop the title screen's,
# but oh well.
# This is fiendishly order-dependent, because the game itself
# is the bottom of the event handling stack, and these go atop
# it.
# Again, oh well!  That's state machines for you.  Especially
# sort of implicit ones.
def doTitleScreen(window):
    logo = resource.getSprite("logo")
    logo.position = (0,0)
    title = resource.getSprite("title")
    title.position = (0,0)

    def draw_logo():
        window.clear()
        logo.draw()
        return True

    def draw_title():
        window.clear()
        title.draw()
        return True

    def on_key_press(key, modifiers):
        window.pop_handlers()
        return True

    window.push_handlers(on_draw=draw_title, on_key_press=on_key_press)
    window.push_handlers(on_draw=draw_logo, on_key_press=on_key_press)
        

def doGameOver(window):
    gameover = resource.getSprite("gameover")
    gameover.position = (0,0)

    # Pop off the actual game handlers
    window.pop_handlers()

    def on_draw():
        window.clear()
        gameover.draw()
        return True

    def doClose(dt):
        window.close()

    window.push_handlers(on_draw)
    pyglet.clock.schedule_once(doClose, 2)


def pushGameEventHandlers(window, gs):
    def on_key_press(key, modifiers):
        if key == pyglet.window.key.Q:
            doGameOver(window)
        gs.player.on_key_press(gs, key)

    def on_key_release(key, modifiers):
        gs.player.on_key_release(gs, key)

    # Add basic handlers for keypresses and releases.
    window.push_handlers(on_key_press, on_key_release)    

def main():
    # TODO: Choose resolution
    screenw = 800
    screenh = 600
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

    pushGameEventHandlers(window, gs)
    doTitleScreen(window)
    pyglet.app.run()


#    statText = "X: {0:5.2f}  Y: {1:5.2f}  Velocity: ({2:5.2f}, {3:5.2f})  Hits: {4}".format(\
#        gs.camerax, gs.cameray, gs.player.parent.vel[0], gs.player.parent.vel[1], gs.player.hits)
#    display = font.render(statText, True, pygame.Color(255, 255, 255), pygame.Color(0,0,0))

if __name__ == '__main__':
    main()
