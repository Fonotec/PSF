#!/usr/bin/env python
import numpy as np


def dedispersion(foldedarray,DM,frequencies,dt=(512*64)/70e6):
    print(DM)
    timedelays = 4.15e-3*DM*(frequencies[0]**(-2)-frequencies**(-2))
    #binshifts = np.round(timedelays/dt)
    binshifts = timedelays/dt
    #Applying the dispersion meassure
    for i in range(len(foldedarray[0,:])-1):
        currentshift = binshifts[i]
        
        # calculate the index
        lowerindex = int(np.floor(currentshift))
        higherindex = lowerindex+1

        # calculate the weight
        higherweigth = currentshift - lowerindex
        lowerweigth = 1- higherweigth
        # add an interpolation when dedispersionss
        foldedarray[:,i+1] = lowerweigth*np.roll(foldedarray[:,i+1],lowerindex) + higherweigth*np.roll(foldedarray[:,i+1],higherindex)    
        #foldedarray[:,i+1] = np.roll(foldedarray[:,i+1],int(currentshift))


    return foldedarray

def pulseProfile(foldedarray,DM,frequencies):
    dedispersed = dedispersion(foldedarray,DM,frequencies)
    return np.sum(dedispersed,axis=1)

