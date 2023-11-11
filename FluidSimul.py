import pygame
import math
import sys
from Particle import Particle
from Ensemble import Ensemble
from Grid import Grid

# pygame setup
pygame.init()
screen = pygame.display.set_mode((720, 560))
clock = pygame.time.Clock()
N = 2
running = True
starting = True

while(running):
    
    for event in pygame.event.get():
        # checking if the user wants to quit
        if(event.type == pygame.QUIT):
            running = False
        # checking if the user wants to change how the mouse behaves
        if(event.type == 1026):
            E.changeMus()

    # fill the screen with a background color, deleting everything from the last frame. 
    screen.fill("black")

    # Render the updating of the particles
    if(not starting):
        E.illustrate()
        for n in range(0,N):
            E.update()

    # flip() puts the changes on the screen
    pygame.display.flip()
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.

    dt = clock.tick(30)/N

    if(starting):
        # constants after dt are: g, pressure, smoothing, mouse factor
    	E = Ensemble(1000,screen,4,10,0.3,dt,9E-5,3E1,2E0,3E-4)
    	starting = False

pygame.quit()