#!/usr/bin/env python
import numpy as np
from numba import njit
import numba as nb

@njit
def moving_average(a, n=3) :
    assert n%2==1
    #b = np.pad(a, (n//2,n//2), 'symmetric')
    b = np.concatenate((a[n//2-1::-1], a, a[:-n//2:-1]))
    ret = np.cumsum(b)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n-1:] / n

@njit
def pyramid_average(a,n=5):
    return moving_average(moving_average(a, n//2+1), n//2+1)

@njit
def flagData(data, nwindow=100001, signific=5, filtertype=0, badneighbors=4):
    # Filtertype: 0 for pyramid, 1 for tophat
    time_num_points, freq_num_points = data.shape
    data = np.copy(data.T) # transpose makes things faster
    indbad = (data==0)
    for i in range(freq_num_points):
        dset = data[i]

        # Smoothing is done in log-space
        # That removes the effect of outliers on the smoothed function.
        if filtertype == 1:
            smoothed=np.exp(moving_average(np.log(dset), n=nwindow))
        else:
            smoothed=np.exp(pyramid_average(np.log(dset), n=nwindow))
        residuals = (dset-smoothed)

        percs = np.percentile(residuals, [25,75])
        std = (percs[1]-percs[0])/1.349 # Use a more robust std estimator

        curind = indbad[i]
        curind |=  residuals > signific*std
        curind |=  residuals < -signific*std
        # For each bad point, also flag its nearest neighbors
        for _ in range(badneighbors):
            curind[1:] = curind[1:] | curind[:-1]
            curind[:-1] = curind[1:] | curind[:-1]

    return np.copy(indbad.T)
