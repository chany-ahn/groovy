import pygame
import time
import numpy as np
import pickle

# Importing data to show visualization
with open('x100_y100_t5000_ru1_rv05_f_055_k062.pkl', 'rb') as f:
  time_array = pickle.load(f)

# x-dimension, y-dimension, number of time steps, number of components = 2
x_dim, y_dim, time, components = time_array.shape


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
# use a rectangle for now, might change later


# create a shape to represent the space and time
def draw_shape(posX, posY, w, h, color):
    pygame.draw.rect(window, color, [posX, posY, w, h])

# WILL HAVE TO PICK A BETTER COLOR MAP FUNCTION
def colorMap(conc1, conc2, prop):
    # Method to determine concentrations of the each cell
    # 0 < conc < 1
    conc1 = conc1
    first_shade = conc1 * 255
    second_shade = conc2 * 255
    # find the average of the two shades
    m = int((first_shade + second_shade) / 2)
    n = int(conc1 * 255)
    l = int(conc2 * 255)
    color = (n,m,l) # intialize the color (black default)
    return color

def updateCells(k):
    # idea of this is to update concs simulatneoulsy so that it displays the "cells"
    # with the current concentrations at a given time step
    # iterate through the time steps
    component_a_2d = time_array[:, :, k, 0] # concentrations of the first component
    component_b_2d = time_array[:, :, k, 1] # concentrations of the second component
    for i in range(0, x_dim):
        for j in range(0, y_dim):
            # drawing rectangles to form cells
            conc1 = component_a_2d[i,j] # conc of comp 1 at space (x,y)
            conc2 = component_b_2d[i,j] # conc of comp 2 at space (x,y)
            prop = float(k / time)
            color = colorMap(conc1, conc2, prop) # determine the color for the specfied cell
            draw_shape(i*width, j*height, width, height, color) # draw the shape

def game_loop():
    running = True # initial condition for the game loop
    k = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        updateCells(k)
        # if k is less than the maximum number of time steps, iterate to the next time step
        if k == time-1:
            pass
        else:
            k += 1
        pygame.display.update()
        clock.tick(20)


game_loop()
