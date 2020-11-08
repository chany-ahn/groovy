import pygame
import random
import numpy as np
import matplotlib.pyplot as plt

wind_dimx = 800
wind_dimy = 600
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
            color = (random.randrange(256), random.randrange(256), random.randrange(256))
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
scaled_arr_left  = [[x//8, y//6] for x, y in pos_arr_left]
scaled_arr_right = [[x//8, y//6] for x, y in pos_arr_right]

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

plt.imshow(frame_0[:,:,1])


'''
pos_arr_lef = np.floor(pos_arr_lef)
#ones = np.ones(pos_arr_lef.shape[0])
if pos_arr_lef.size !=0:
    ones = np.ones(pos_arr_lef.shape[0])
    pos_arr_lef = np.concatenate((pos_arr_lef, np.array(ones)[:,None]),axis=1)


pos_arr_rig = np.array(pos_right)*scale_factor
pos_arr_rig = np.floor(pos_arr_rig)
if pos_arr_rig.size!=0:
    twoes = np.full((pos_arr_rig.shape[0]),2)
    #print(twoes)
    pos_arr_rig  = np.concatenate((pos_arr_rig, np.array(twoes)[:,None]),axis=1)
    

pos_tot = np.concatenate((pos_arr_lef, pos_arr_rig), axis = 0)

print(pos_arr_lef.shape)
print(pos_arr_rig.shape)
print(pos_tot.shape)

##the unique array 
[pos_un, ret] = np.unique(pos_tot,return_index = True, axis =0 )
print("\n")
print(pos_un)
print("\n")

x = np.arange( 0,101,1)
y = np.arange( 0,101,1)
xy = np.zeros((100,100))

for index,values in enumerate(pos_un):
    #print(values)
    x_cur = int(values[0])
    y_cur = int(values[1])
    if xy[x_cur][y_cur] == 0:
        xy[x_cur][y_cur] = int(values[2])
    elif xy[x_cur][y_cur] != 0:
        xy[x_cur][y_cur] = 3



xx, yy = np.meshgrid(x, y)


for index,values in enumerate(pos_un):
    #print(values)
    x_cur = int(values[0])
    y_cur = int(values[1])
    if xx[x_cur][y_cur] == 0:
        xx[x_cur][y_cur] = int(values[2])
    elif xx[x_cur][y_cur] != 0:
        xx[x_cur][y_cur] = 3

plt.scatter(xx,yy)
'''





pygame.quit()