import pygame
import time
import numpy as np

# Arrays for the diffusion data
time_array = np.zeros((4,4,4,2))
# x-dimension, y-dimension, number of time steps, number of components = 2
# x_dim, y_dim, time, components = time_array.shape 
x_dim = 40
y_dim = 40
#Initialize pygame
pygame.init()

#Create window with the same number 
window_dim = 800 # dimension for the window
window = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock() # clock to set frame rate

# Set up the number of components that are going to show up in the window
# number of cells in each dimension for space (should be the same)
width = int(window_dim/x_dim)
height = int(window_dim/y_dim)
print(str(width) + " " + str(height))
# use a rectangle for now, might change later


# create a shape to represent the space and time
def draw_shape(posX, posY, w, h, color):
    pygame.draw.rect(window, color, [posX, posY, w, h])

def updateConc():
    # idea of this is to update concs simulatneoulsy so that it displays the "cells"
    # with the current concentrations at a given time step
    red = (255,0,0)
    for i in range(0,window_dim, width):
        for j in range(0, window_dim, height):
            # drawing rectangles to form a grid
            draw_shape(i, j, width, height, red)

def game_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        updateConc()
        pygame.display.update()
        clock.tick(60)

game_loop()
