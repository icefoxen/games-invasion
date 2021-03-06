#!/usr/bin/env python

import pyglet
import pyglet.text
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
    w = window.width
    h = window.height
    logo = resource.getSprite("logo")
    logo.position = (w/2,h/2)
    logo.scale = float(w) / float(logo.width)
    title = resource.getSprite("title")
    title.position = (w/2,h/2)
    title.scale = float(w) / float(title.width)

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
    gameover.position = (window.width/2,window.height/2)
    gameover.scale = float(window.width) / float(gameover.width)

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
        if key == pyglet.window.key.ESCAPE:
            doGameOver(window)
            return True
        gs.player.on_key_press(gs, key)

    def on_key_release(key, modifiers):
        gs.player.on_key_release(gs, key)

    # Add basic handlers for keypresses and releases.
    window.push_handlers(on_key_press, on_key_release)    

class GUI(object):
    def __init__(s, gs):
        s.gs = gs
        s.hitsLabel = pyglet.text.Label(text='foo', x=10, y=10)

    def update(s, dt):
        s.hitsLabel.text = "Hits: {}".format(s.gs.player.hits)

    def draw(s):
        s.hitsLabel.draw()

def main():
    # TODO: Choose resolution
    screenw = 1024
    screenh = 768
    window = pyglet.window.Window(width=screenw, height=screenh)
    window.set_vsync(False)
    # XXX: The animation state here is a little wibbly, work on it.
    #doTitleScreen(window)

    gs = GameState(screenw, screenh)
    fpsDisplay = pyglet.clock.ClockDisplay()
    gui = GUI(gs)

    @window.event
    def on_draw():
        window.clear()
        gs.background.draw(gs)
        gs.player.draw(gs)
        for p in gs.particles:
            p.draw(gs)
        for p in gs.planets:
            p.draw(gs)
            for f in p.surfFeatures:
                f.draw(gs)
        fpsDisplay.draw()
        gui.draw()

    def updateGame(dt):
        if not gs.player.alive:
            doGameOver(window)
        else:
            gs.update(dt)
            gui.update(dt)
    
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
