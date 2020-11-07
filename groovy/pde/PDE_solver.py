import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
import pickle


def time_step(frame_t1, dt, lap, ru, rv, f, k, boundary='constant'):
    '''function to move an initial grid of concentrations forward through the reaction-diffusion equations by
       a single time step dt.

       Parameters
       ----------
       frame_t1: an (N x M x 1 x Q) numpy array where N,M are the lengths of the two spatial components,
                 and Q is the number of reactants.
       dt:       float, the length of the time step
       lap:      2D numpy array, the (I x J) kernel that will be convolved with the concentrations in place of
                 performing a Laplacian.
       ru/rv:    the diffusion constants for reactant U and reactant V, respectively
       f:        float, the rate constant for the supply of reactant U
       k:        float, the rate constant for the removal of reactant V
       boundary: 'constant', 'reflect', 'nearest', 'mirror', or 'wrap' (mode parameter in scipy.ndimage.convolve)
                 'constant' will give hard boundaries and 'wrap' will give periodic boundary conditions

       returns
       -------
       frame_t2: an (N x M x Q) numpy array where N,M are the lengths of the two spatial components,
                 and Q is the number of reactants. This will be frame_t1 moved forward by a time step dt

    '''

    # start by moving U forward one time step
    lapu = convolve(frame_t1[:,:,0,0], lap, mode=boundary, cval=0.0)
    diffterm = ru * lapu
    diffterm = diffterm[:,:,np.newaxis]

    reactterm = frame_t1[:,:,:,0] * frame_t1[:,:,:,1]**2

    sourceterm = f*(1 - frame_t1[:,:,:,0])

    frame_t2 = frame_t1[:,:,:,0] + (diffterm - reactterm + sourceterm)*dt

    # move V forward one time step
    lapv = convolve(frame_t1[:,:,0,1], lap, mode=boundary, cval=0.0)
    diffterm = rv * lapv
    diffterm = diffterm[:,:,np.newaxis]

    # same reactterm as for U

    sinkterm = (f + k)*frame_t1[:,:,:,1]

    frame_t2 = np.stack((frame_t2, frame_t1[:,:,:,1] + (diffterm + reactterm - sinkterm)*dt), axis=-1)

    return frame_t2




def evolve(frame_t0, dt, nsteps, slicestep, lap, ru, rv, f, k, boundary='constant'):
    '''function to move an initial grid of concentrations forward through the reaction-diffusion equations by
       a single time step dt.

       Parameters
       ----------
       frame_t0: an (N x M x Q) numpy array where N,M are the lengths of the two spatial components,
                 and Q is the number of reactants. This should be the initial conditions
       dt:       float, the length of the time step
       nsteps:   int, the number of single time steps the function should move the system forward
       slicestep:int, the final array will be returned thinned so as to make it more manageable to animate and save
                 as a file. This gives the number of frames that should be skipped before keeping one.
       lap:      2D numpy array, the (I x J) kernel that will be convolved with the concentrations in place of
                 performing a Laplacian.
       ru/rv:    the diffusion constants for reactant U and reactant V, respectively
       f:        float, the rate constant for the supply of reactant U
       k:        float, the rate constant for the removal of reactant V
       boundary: 'constant', 'reflect', 'nearest', 'mirror', or 'wrap' (mode parameter in scipy.ndimage.convolve)
                 'constant' will give hard boundaries and 'wrap' will give periodic boundary conditions

       returns
       -------
       final:    an (N x M x P x Q) numpy array where N,M are the lengths of the two spatial components,
                 Q is the number of reactants, and P=nsteps. This will be frame_t0 moved forward through a total
                 length of time dt*nsteps

    '''

    # start with the initial frame as the 0th entry
    frame_tlast = frame_t0
    final = frame_t0

    # iterate through (1, nsteps), each time creating a new frame by moving the most recent frame forward through
    # time by dt and then appending this new frame onto the final array
    for step in range(nsteps):

        frame_tnext = time_step(frame_tlast, dt, lap, ru, rv, f, k, boundary=boundary)
        final = np.concatenate((final, frame_tnext), axis=2)

        frame_tlast = frame_tnext

        if step % 1000 == 0:
            print(step)


    # thin out the data in the time axis - only keep one in every slicestep frames (to make it better to animate)
    frameslice = np.arange(0, nsteps+1, slicestep)

    finalslice = final[:,:,frameslice,:]

    return finalslice
