#!/usr/bin/env python
import numpy as np
import scipy.optimize as sco

def dedispersion(foldedarray,DM,frequencies,dt=(512*64)/70e6):
    timedelays = 4.15e-3*DM*(frequencies[0]**(-2)-frequencies**(-2))
    #binshifts = np.round(timedelays/dt)
    binshifts = timedelays/dt
    #Applying the dispersion meassure
    for i in range(len(foldedarray[0,:])):
        currentshift = binshifts[i]
        
        # calculate the index
        lowerindex = int(np.floor(currentshift))
        higherindex = lowerindex+1

        # calculate the weight
        higherweigth = currentshift - lowerindex
        lowerweigth = 1- higherweigth
        # add an interpolation when dedispersions
        foldedarray[:,i] = lowerweigth*np.roll(foldedarray[:,i],lowerindex) + higherweigth*np.roll(foldedarray[:,i],higherindex)
        #foldedarray[:,i+1] = np.roll(foldedarray[:,i+1],int(currentshift))


    return foldedarray

def pulseProfile(foldedarray,DM,frequencies):
    dedispersed = dedispersion(foldedarray,DM,frequencies)
    return np.sum(dedispersed,axis=1)

def fitDM(foldedarray,frequencies,dt=(512*64)/70e6):

    maxchannel = np.argmax(foldedarray,axis=0)

    fitresults = sco.curve_fit(DMfunction,frequencies[10:100],maxchannel[10:100],p0=[10,1000,frequencies[0]])


    return maxchannel,fitresults

def DMfunction(freq,DM,A,freqmin):
    return 4.15e-3*DM*(freqmin**(-2)-freq**(-2))+A
