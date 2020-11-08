import pygame
import random
import numpy as np
import matplotlib.pyplot as plt

def user_input():
    # frame_0 is gonna be the input frame for the evolve function

    wind_dimx = 800
    wind_dimy = 800
    screen = pygame.display.set_mode((wind_dimx, wind_dimy))

    draw_on = False
    last_pos = (0, 0)
    color = (255, 128, 0)
    radius = 10

    ##this will just draw a circle

    def roundline(srf, color, start, end, radius=1):
        dx = end[0]-start[0]
        dy = end[1]-start[1]
        distance = max(abs(dx), abs(dy))
        for i in range(distance):
            x = int( start[0]+float(i)/distance*dx)
            y = int( start[1]+float(i)/distance*dy)
            pygame.draw.circle(srf, color, (x, y), radius)


    #the list will save the tuples of the mouse position
    pos_mouse = np.zeros(shape =(10,2))
    pos_left = list()
    pos_right = list()

    try:
        while True:
            cur_eve = pygame.event.wait()
            mouse_pos = pygame.mouse.get_pos()
            left_click, middle_click, right_click =  pygame.mouse.get_pressed()
            if cur_eve.type == pygame.QUIT:
                raise StopIteration
                ##the first if satements is if the button is pressed
            if cur_eve.type == pygame.MOUSEBUTTONDOWN:
                if left_click:
                    color = (255, 0, 0)
                else:
                    color = (0, 0, 255)
                pygame.draw.circle(screen, color, cur_eve.pos, radius)
                draw_on = True
                ##if you are not clicking on the mouse 
            if cur_eve.type == pygame.MOUSEBUTTONUP:
                draw_on = False
            if draw_on == True:
                #saves the positions depending if it is a right click or left click
                if left_click == True:
                    pos_left.append(mouse_pos)
                elif right_click == True:
                    pos_right.append(mouse_pos)
            if cur_eve.type == pygame.MOUSEMOTION:
                if draw_on:
                    pygame.draw.circle(screen, color, cur_eve.pos, radius)
                    roundline(screen, color, cur_eve.pos, last_pos,  radius)
                last_pos = cur_eve.pos
            pygame.display.flip()

    except StopIteration:
        pass

    pos_arr_left = np.array(pos_left)
    pos_arr_right = np.array(pos_right)

    # Scales down what we need
    scaled_arr_left  = [[x//8, y//8] for x, y in pos_arr_left]
    scaled_arr_right = [[x//8, y//8] for x, y in pos_arr_right]

    # Create the output
    frame_0 = np.zeros((100, 100, 2))

    # Populate by species 1
    for x, y in scaled_arr_left:
        frame_0[x, y, 0] = 1

    # Populate by species 2
    for x, y in scaled_arr_right:
        if frame_0[x, y, 0] != 0:
            frame_0[x, y, 0] = 0.5
            frame_0[x, y, 1] = 0.5
        else:
            frame_0[x, y, 1] = 1

    # plt.imshow(frame_0[:,:,1])

    pygame.quit()

    return frame_0