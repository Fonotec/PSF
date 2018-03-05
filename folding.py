#!/usr/bin/env python
import numpy as np
import math as ma
from tqdm import tqdm # A nice progress bar, can be installed using, even on astro computers with: pip install --user tqdm

dt = (512*64)/(70e6)

def timeFolding(data_array,nbins,period,flagged, progressbar=True):
    stepsize = dt*nbins/period
    # Making sure counting starts at 0
    data_array[:,0] = data_array[:,0]-np.min(data_array[:,0]) 

    # The shape of the data
    time_num_points, freq_num_points = data_array.shape
    
    #Arrays for folding and normalization
    foldedarray = np.zeros((nbins,256))
    normalarray = np.zeros((nbins,256))


    # Timearray in units of bin
    bindata = np.arange(0,time_num_points*stepsize,stepsize)

    # Modulus bin data array
    # This saves us a for loop.
    bindatamod = np.mod(bindata,nbins)
    
    ###################################
    # 4. Folding for loop  ############
    ###################################

    # Start the for loop and loop through
    # all the time steps
    iterator = tqdm(range(time_num_points)) if progressbar else range(time_num_points)
    for i in iterator:
        # Calculate the weight of the lower index and the 
        # higher index. In general when we have the index 
        # 421.4, this will mean that index 421 will get norm
        # 0.6 and index 422 will get norm 0.4, this way
        # we are interpolating linearly between the higher and 
        # the lower value, and this will increase the accuracy
        # of our folding algorithm.
        lowernorm = np.repeat(ma.ceil(bindatamod[i])-bindatamod[i],freq_num_points)
        # because the total norm is conserved we can simply 
        # subtract the lower norm from 1. 
        highernorm = 1-lowernorm
        # Determine the lower index by using floor
        indexlow = int(ma.floor(bindatamod[i]))
        # Determine the higher index by just adding 1.
        indexhigh = indexlow + 1
        
        # Neglect the flagged indices by setting the normalization 
        # factors to 0
        highernorm[flagged[i]] = 0
        lowernorm[flagged[i]] = 0
        ## Storing the data ##

        # Here we store the for the lower index with the 
        # appropriate weighting factor 
        #print(lowernorm.shape, data_array.shape, foldedarray.shape)
        foldedarray[indexlow,:] += lowernorm*data_array[i,:]
        # We do this similar for the normalization factor which
        # we store to normalize the data later on.
        normalarray[indexlow,:] += lowernorm
        
        # For the higher index it is slightly more complicated
        # because the higher index can be higher than the 
        # number of bins one time for every pulse, to prevent
        # this we take the modulus with the number of bins
        # this results in a natural reduction back to the 
        # first index
        # Storing the folded data for the higher index        
        foldedarray[np.mod(indexhigh,nbins),:] += highernorm*data_array[i,:]
        # storing the weight factor for the higher index
        normalarray[np.mod(indexhigh,nbins),:] += highernorm

    ## Finishing the loop ##

    # After the loop of normalize the data, to prevent
    # that points in the array are counted more often
    protonormalisedfoldedarray = foldedarray/normalarray

    # normalize the data by dividing by the sum
    normalisedfoldedarray = np.divide( protonormalisedfoldedarray, np.sum(protonormalisedfoldedarray,axis=0) )    
    
    return normalisedfoldedarray
