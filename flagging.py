#!/usr/bin/env python
import numpy as np

dt = (64*512)/(70e6)
def moving_average(a, n=3) :
    assert n%2==1
    b = np.pad(a, (n//2,n//2), 'symmetric')
    ret = np.cumsum(b, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n-1:] / n

def pyramid_average(a,n=5):
    return moving_average(moving_average(a, n//2+1), n//2+1)

def flagData(data, nwindow=100001, signific=5):
    time_num_points, freq_num_points = data.shape
    indbad = (data==0)
    for i in range(freq_num_points):
        dset = data[:,i]
        smoothed=pyramid_average(dset, n=nwindow)
        residuals = (dset-smoothed)
        std = residuals.std()
        indbad[:,i] |=  residuals > signific*std
        indbad[:,i] |=  residuals < -signific*std
    return indbad
