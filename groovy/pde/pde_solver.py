import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
import pickle
from tqdm.auto import tqdm


def time_step(frame_t1, lap, ru, rv, f, k, dt=1, boundary='constant'):
    '''function to move an initial grid of concentrations forward through the reaction-diffusion equations by
       a single time step dt.

       Parameters
       ----------
       frame_t1: an (N x M x 1 x Q) numpy array where N,M are the lengths of the two spatial components,
                 and Q is the number of reactants.
       dt:       float, the length of the time step
       lap:      2D numpy array, the (I x J) kernel that will be convolved with the concentrations in place of
                 performing a Laplacian.
       ru/rv:    the diffusion constants for reactant U and reactant V, respectively. Relevant ranges are
                 0 <= ru/rv <= 1
       f:        float, the rate constant for the supply of reactant U. Relevant ranges are 0 <= f <= 0.1
       k:        float, the rate constant for the removal of reactant V. Relevant ranges are 0 <= k <= 0.1
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




def evolve(frame_t0, ru, rv, f, k, dt=1, nsteps=5000, slicestep=50, lap=None, boundary='constant'):
    '''function to move an initial grid of concentrations forward through the reaction-diffusion equations by
       a single time step dt.

       Parameters
       ----------
       frame_t0: an (N x M x Q) numpy array where N,M are the lengths of the two spatial components,
                 and Q is the number of reactants. This should be the initial conditions
       ru/rv:    the diffusion constants for reactant U and reactant V, respectively. Relevant ranges are
                 0 <= ru/rv <= 1
       f:        float, the rate constant for the supply of reactant U. Relevant ranges are 0 <= f <= 0.1
       k:        float, the rate constant for the removal of reactant V. Relevant ranges are 0 <= f <= 0.1
       dt:       float, the length of the time step (defalt: 1)
       nsteps:   int, the number of single time steps the function should move the system forward (default: 5000)
       slicestep:int, the final array will be returned thinned so as to make it more manageable to animate and save
                 as a file. This gives the number of frames that should be skipped before keeping one. (default:50)
       lap:      2D numpy array, the (I x J) kernel that will be convolved with the concentrations in place of
                 performing a Laplacian. If none is passed, -1 will be used for the center value, 0.2 will be used
                 for 4-connected pixels, and 0.05 will be used for 8-connected pixels

       boundary: 'constant', 'reflect', 'nearest', 'mirror', or 'wrap' (mode parameter in scipy.ndimage.convolve)
                 'constant' will give hard boundaries and 'wrap' will give periodic boundary conditions

       returns
       -------
       final:    an (N x M x P x Q) numpy array where N,M are the lengths of the two spatial components,
                 Q is the number of reactants, and P=nsteps. This will be frame_t0 moved forward through a total
                 length of time dt*nsteps

    '''

    # if a Laplacian kernel isn't passed, define it with the default values
    if not lap:
        lap = np.array([[0.05, 0.2, 0.05],
                        [0.2, -1, 0.2],
                        [0.05, 0.2, 0.05]]) # values suggested by https://www.karlsims.com/rd.html

    # start with the initial frame as the 0th entry
    frame_tlast = frame_t0
    final = frame_t0

    # iterate through (1, nsteps), each time creating a new frame by moving the most recent frame forward through
    # time by dt and then appending this new frame onto the final array
    for step in tqdm(range(nsteps-1), desc='Time steps', leave=False):

        frame_tnext = time_step(frame_tlast, lap, ru, rv, f, k, dt=dt, boundary=boundary)
        final = np.concatenate((final, frame_tnext), axis=2)

        frame_tlast = frame_tnext


    # thin out the data in the time axis - only keep one in every slicestep frames (to make it better to animate)
    frameslice = np.arange(0, nsteps, slicestep)

    finalslice = final[:,:,frameslice,:]

    return finalslice
