#!/usr/bin/env python

import pygame
from pygame.locals import *
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
def doTitleScreen(surf):
    logo = resource.loadImage("logo")
    title = resource.loadImage("title")
    surf.fill(pygame.Color(0, 0, 0))
    surf.blit(logo, (0, 0))
    pygame.display.flip()
    pygame.time.wait(2000)

    surf.fill(pygame.Color(0, 0, 0))
    surf.blit(title, (0, 0))
    pygame.display.flip()
    pygame.event.clear()
    while True:
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                return

def doGameOver(surf):
    gameover = resource.loadImage("gameover")
    surf.fill(pygame.Color(0, 0, 0))
    surf.blit(gameover, (0, 0))
    pygame.display.flip()
    pygame.time.wait(2000)
    
    
def mainloop(screenw, screenh):
    surf = pygame.display.set_mode((screenw, screenh), 0, 0)
    font = pygame.font.Font("data/FreeMono.ttf", 14)
    doTitleScreen(surf)

    gs = GameState(screenw, screenh)
    lastframe = pygame.time.get_ticks()
    framecount = 0
    pygame.event.clear()
    while gs.gameRunning:
        # Clear screen
        surf.fill(pygame.Color(0, 0, 0))

        # Handle timer
        # dt is in seconds
        now = pygame.time.get_ticks()
        dt = (now - lastframe) / 1000.0
        lastframe = now
        framecount += 1

        # Handle input
        handleInput(gs)

        # Update game state
        gs.update(dt)

        # Draw stuff
        gs.background.draw(surf, gs)
        gs.player.draw(surf, gs)

        for p in gs.particles:
            p.draw(surf, gs)
        for p in gs.planets:
            p.draw(surf, gs)
            for f in p.surfFeatures:
                f.draw(surf, gs)
        statText = "X: {0:5.2f}  Y: {1:5.2f}  Velocity: ({2:5.2f}, {3:5.2f})  Hits: {4}".format(\
            gs.camerax, gs.cameray, gs.player.parent.vel[0], gs.player.parent.vel[1], gs.player.hits)
        display = font.render(statText, True, pygame.Color(255, 255, 255), pygame.Color(0,0,0))
        surf.blit(display, (0, 0))

        pygame.display.flip()

    if not gs.player.alive:
        doGameOver(surf)

    seconds = pygame.time.get_ticks() / 1000.0
    fps = framecount / seconds
    print("Game ran %s seconds, average %s fps" % (seconds, fps))
    print("Thank you for playing!")
    print("This might crash on Windows; I can't seem to fix it.  :-(")
    


def main():
    pygame.init()
    #pygame.font.init()
    # TODO: Choose resolution
    mainloop(800, 600)
    #cProfile.run('mainloop(800, 600)')

    # Called when interpreter exits anyway
    #pygame.quit()


if __name__ == '__main__':
    main()
