import pygame
import time
import numpy as np
import pickle

# Importing data to show visualization
with open('x100_y100_t5000_ru1_rv05_f_055_k062_periodic.pkl', 'rb') as f:
  time_array = pickle.load(f)

# x-dimension, y-dimension, number of time steps, number of components = 2
x_dim, y_dim, time, components = time_array.shape

#Initialize pygame
pygame.init()

#Create window with the same number 
window_dim = 800 # dimension for the window
window = pygame.display.set_mode((window_dim, window_dim))
clock = pygame.time.Clock() # clock to set frame rate

# Set up the number of components that are going to show up in the window
# number of cells in each dimension for space (should be the same)
width = int(window_dim/x_dim)
height = int(window_dim/y_dim)

# create a shape to represent the space and time
def draw_shape(posX, posY, w, h, color):
    pygame.draw.rect(window, color, [posX,posY,w,h]) # rectangle
    #pygame.draw.circle(window, color, (posX, posY), int(w/2)) # circle

def colorMap(conc1, conc2):
    # Method to determine concentrations of the each cell
    # 0 < conc < 1  -> 0 <= conc1 + conc2 <= 2
    r = conc1 * 255
    g = 0
    b = conc2 * 255
    color = (r,g,b)
    return color

def displayGradient():
    # draw a border
    draw_shape(window_dim - 257, 0, 256,258, (255,255,255))
    for i in range(256):
        for j in range(256):
                draw_shape(window_dim - 255 + i,255-j,1,1,(i,0,j))
    # time for captions
    font = pygame.font.Font('OpenSans-Regular.ttf', 12)

    conc1 = font.render("Conc. Component A", True, (255,255,255))
    conc2 = font.render("Conc. Component B", True, (255,255,255))
    conc1Rect = conc1.get_rect()
    conc2Rect = conc2.get_rect()
    conc1Rect.center = (window_dim - 258 - int(conc1Rect.width/2), int(255/2))
    conc2Rect.center = (window_dim - int(255/2), 267)
    window.blit(conc1, conc1Rect)
    window.blit(conc2, conc2Rect)

def updateCells(k):
    # idea of this is to update concs simulatneoulsy so that it displays the "cells"
    # with the current concentrations at a given time step
    # iterate through the time steps
    component_a_2d = time_array[:, :, k, 0] # concentrations of the first component
    component_b_2d = time_array[:, :, k, 1] # concentrations of the second component
    for i in range(0, int(x_dim)):
        for j in range(0, int(y_dim)):
            # drawing rectangles to form cells
                if i*width > window_dim - 255 and j*height < 255:
                    pass
                else:
                    conc1 = component_a_2d[i,j] # conc of comp 1 at space (x,y)
                    conc2 = component_b_2d[i,j] # conc of comp 2 at space (x,y)
                    color = colorMap(conc1, conc2) # determine the color for the specfied cell
                    draw_shape(i*width, j*height, width, height, color) # draw the shape



def game_loop():
    running = True # initial condition for the game loop
    k = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        updateCells(k)
        displayGradient()
        # if k is less than the maximum number of time steps, iterate to the next time step
        if k != time-1:
            k += 1
        pygame.display.update()
        clock.tick(60)

# call the game loop
game_loop()
pygame.quit()

