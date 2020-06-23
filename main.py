import pygame
import os
import grid
import time
import numpy as np
import button

os.environ["SDL_VIDEO_CENTERED"] = '1'
width, height = 1800, 1000
size = (width, height)

pygame.init()
pygame.display.set_caption("Conway game of life")
screen =  pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 20

black = (0, 0, 0)
blue = (0, 14, 71)
white = (255,255,255)

scaler = 40
offset = 1

Grid = grid.Grid(width, height, scaler, offset)
Grid.random2d_array()

run = True
newSurface = pygame.Surface((500,300))

greenButton = button.Button((0,255,0), 255,255 , 250, 100, 'slow')
while run:
    clock.tick(fps)
    screen.fill(black)
    greenButton.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    Grid.Conway(off_color=white, on_color=blue, surface=newSurface)
    screen.blit(newSurface,(0,0))
    pygame.display.update()
pygame.quit()

