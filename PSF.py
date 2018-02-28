#!/usr/bin/env python
# coding: utf-8
# importing all the used modules
import numpy as np
import math as ma
import time
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, show
import scipy as sc
import scipy.optimize as sco
import sys
from startscreen import startScreen

###################################
## PSF (Pulsar Spectral Folder) ###
###################################
## VERSION 1.0.1 ##################
###################################
## This code is written by       ##
## Roi Kugel and Folkert Nobels  ##
## Designed Specifically to work ##
## With the Dwingeloo Radio      ##
## Telescope of CAMRAS           ##
###################################
# The goal of this code is to determine 
# the pulse profile of observed pulsars.
# In observing pulsars there are in general
# Only 2 free parameters. The first being 
# the period of the pulsar or P or P0 in 
# the literature. And the dispersion measure
# that describes how much the different 
# frequencies are retarded due to the influence
# of the free electrons in the interstellar 
# medium between the Earth and the pulsar. 
# The dispersion measure is often written as
# DM and can have values ranging from 2 till 
# 100+ for more distant pulsars.

startScreen('1.0.1')

###################################
## LAYOUT OF THE PROGRAM ##########
###################################
# The code consist of several parts: 
# 1. Asking/giving the required input parameters.
#    1.1    Interactive options
# 2. Loading the data and resizing the data.
# 3. Initilizing the folding variables.
# 4. Folding for all dimension for the given input
#    parameter for the period.
# 5. Display a slice in time, this will give you 
#    This will give you the spectral sensitivity     
# 6. Normalize the signals more
# 7. Display  specific channels
# 8. Storing a rainfall image of the data
# 9. Calculate the Dispersion Measure

###################################
# 1. Input parameters #############
###################################
t1 = time.time()

#stats_dict={"PSRB054": (0.71452, 20.7), "PSRB2016": (0.55795348, 14.20), "PSRB1929": (0.226518, 0.20), "PSRJ2145": (0.016052, 9.00 ), 
#            "PSRB1859": 0.655450, 0.3, "PSRB2154": (1.525266, 71.12), "PSRB1946": (0.717311, 129.3)}

# The period of the pulsar          
#period = 0.71452    #PSRB054         
period = 0.55795348  #PSRB2016         
#period = 0.226518   #PSRB1929        
#period = 0.016052   #PSRJ2145                
#period = 0.655450   #PSRB1859
#period = 1.525266   #PSRB2154
#period = 0.717311   #PSRB1946

# The dispersion measure of the pulsar
#DM = 20.7      #PSRB054
DM = 14.20  #PSRB2016
#DM = 0.20  #PSRB1929
#DM = 9.00  #PSRJ2145
#DM = 0.3  #PSRB1859
#DM = 71.12  #PSRB2154
#DM = 129.37  #PSRB1946

# Time resolution of the telescope
dt = (512*64)/(70e6)

# Array with the bandwith
frequencyarray = np.linspace(0.402,0.433,255)

###################################
# 1.1 INTERACTIVE OPTIONS #########
###################################
# If the computation time of every step needs 
# to be shown the following variable should be 
# set to True
comptime = False

# Do you want to interactively display plots?
interacticeplots = False

# Display a time slice to investigate
# the sensitivity?
timeslice = True
# the investigated slot number
timeslot = [0]
timeslot = np.array(timeslot)

# Display individual pulses in channels?
indchannels = True
# Channels to display
channels = [80,90,100]
channels = np.array(channels)

# Calculate the rainfall
rainfall = True

# Dispersion measure parameters
inversesquare = False
linearcase = True
# print the best fit results
bestfitDM = True
#cheap DM fitting 
DMROI = True

t2 = time.time()
if comptime==True:
    print('part 2 =',t2-t1)


###################################
# 2. Loading data #################
###################################
# determine start time
t1 = time.time()
# The data obtained by the Dwingeloo radio
# radio telescope is rather cumbersome and 
# stored as unsigned ints, because of this 
# it is required that a new data type is 
# defined that is an unsigned 32 bit integer
# number:
unsingeddatat = np.dtype(np.uint32)

# Because the endianness of Dwingloo telescope
# is different than the endianness on our 
# machines we need to change the byte order:
unsingeddatat = unsingeddatat.newbyteorder('S')
# for more information regarding endiannes see
# https://en.wikipedia.org/wiki/Endianness

# After constructing the correct data type we can
# load the data by using fromfile.
try:
    myarray = np.fromfile('B0329 54.2016.11.18.1038.5min.dat',dtype=unsingeddatat)
    #myarray = np.fromfile('PSRB1929+10.raw',dtype=unsingeddatat)
    #myarray = np.fromfile('PSR_J2145-0750.raw',dtype=unsingeddatat)
    #myarray = np.fromfile('PSR_B1859+03.raw',dtype=unsingeddatat)
    #myarray = np.fromfile('PSR_B2154+40.raw',dtype=unsingeddatat) #might be shite
    #myarray = np.fromfile('PSR_B2016+28.raw',dtype=unsingeddatat)
    #myarray = np.fromfile('PSR_B1946+35.raw',dtype=unsingeddatat)
    #myarray = np.fromfile('PSR_B1946+35.raw',dtype=unsingeddatat)
    #myarray = np.fromfile('PSR_B0329+54.raw',dtype=unsingeddatat)
    #myarray = np.fromfile('B2016+28_406MHz_2017-12-30.raw',dtype=unsingeddatat)
except FileNotFoundError:
    print("This file could not be found.")
    exit(0)
    
# Until now the data is just a 1 times many array, 
# which is quite useless for our analysis. We want 
# that the data is stored as time vertical and horizontal 
# the frequency bins. 
# We know that we have 256 seperate colums of which the
# 0th element is an arbitary counter and the remaining
# ones are the frequency bins. 
# This means the array needs to be reshaped as follows:
twodarray = np.reshape(myarray,(int(len(myarray)/256),256))

# determine end time with option of displaying computation time
t2 = time.time()
if comptime==True:
    print('Computational time')
    print('part 1 =',t2-t1)


###################################
# 3. Initializing variables  ######
###################################
t1 = time.time()

# Making sure counting starts at 0
twodarray[:,0] = twodarray[:,0]-np.min(twodarray[:,0]) 

# Number of bins per period
nbins = int(round(period/dt))

#Arrays for folding and normalization
foldedarray = np.zeros((nbins,256))
normalarray = np.zeros((nbins,256))

# Stepsize in units of bin
stepsize = dt*nbins/period

# Timearray in units of bin
bindata = np.arange(0,len(twodarray[:,0])*stepsize,stepsize)

# Modulus bin data array
# This saves us a for loop.
bindatamod = np.mod(bindata,nbins)

t2 = time.time()
if comptime==True:
    print('part 3 =',t2-t1)

###################################
#Time based RFI removal ###########
###################################

fig = figure(figsize=(20,10))
frame = fig.add_subplot(1,1,1)
frame.plot(bindata,np.log10(twodarray[:,100]))
show()

###################################
# 4. Folding for loop  ############
###################################
t1 = time.time()
# Start the for loop and loop through
# all the time steps
for i in range(len(bindata)):
    # Calculate the weight of the lower index and the 
    # higher index. In general when we have the index 
    # 421.4, this will mean that index 421 will get norm
    # 0.6 and index 422 will get norm 0.4, this way
    # we are interpolating linearly between the higher and 
    # the lower value, and this will increase the accuracy
    # of our folding algorithm.
    lowernorm = (ma.ceil(bindatamod[i])-bindatamod[i])
    # because the total norm is conserved we can simply 
    # subtract the lower norm from 1. 
    highernorm = 1-lowernorm
    # Determine the lower index by using floor
    indexlow = int(ma.floor(bindatamod[i]))
    # Determine the higher index by just adding 1.
    indexhigh = indexlow + 1
    
    ## Storing the data ##

    # Here we store the for the lower index with the 
    # appropriate weighting factor 
    foldedarray[indexlow,:] += lowernorm*twodarray[i,:]
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
    foldedarray[np.mod(indexhigh,nbins),:] += highernorm*twodarray[i,:]
    # storing the weight factor for the higher index
    normalarray[np.mod(indexhigh,nbins),:] += highernorm
t2 = time.time()

## Finishing the loop ##

# After the loop of normalize the data, to prevent
# that points in the array are counted more often
protonormalisedfoldedarray = foldedarray/normalarray

t2 = time.time()
if comptime==True:
    print('part 4 =',t2-t1)

###################################
# 5. Display a slice in time ######
###################################
if timeslice == True:
    t1 = time.time()
    for i in range(0,len(timeslot)):
        plt.plot(np.log10(protonormalisedfoldedarray[timeslot[i],:]))
    plt.savefig('timeprofileslice.png')
    if interacticeplots==True:
        plt.show()
    plt.close()
    t2 = time.time()
    if comptime==True:
        print('part 5 =',t2-t1)


###################################
# 6. Normalize the signals more ###
###################################
t1 = time.time()

# normalize the data by dividing by the sum
normalisedfoldedarray = np.divide( protonormalisedfoldedarray, np.sum(protonormalisedfoldedarray,axis=0) )

t2 = time.time()
if comptime==True:
    print('part 6 =',t2-t1)

###################################
# 7. Display  specific channels ###
###################################

if indchannels==True:
    t1 = time.time()
    periodtime = np.linspace(0,period,nbins)
    for i in range(0,len(channels)):
        plt.plot(periodtime,normalisedfoldedarray[:,channels[i]])
    plt.savefig('channelprofile.png')
    if interacticeplots:
        plt.show()
    plt.close()
    t2 = time.time()
    if comptime==True:
        print('part 7 =',t2-t1)




###################################
# 8. Display the rainfall #########
###################################
if rainfall == True:
    t1 = time.time()
    plt.matshow(normalisedfoldedarray[:,:150])
    plt.savefig('result3.png')
    if interacticeplots:
        plt.show()
    plt.close()
    t2 = time.time()
    if comptime==True:
        print('part 8 =',t2-t1)


#######################################
# 9. Calculate the Dispersion Measure #
#######################################
t1 = time.time()

# This part of the code has as main use to  
# calculate the dispersion measure, in general
# the electrons between the pulsar and Earth 
# delay the time of the pulses according to 
# a time difference properotional to \nu^-2:
#
#                   DM
# \tau = ------------------------- seconds   (1)
#        2.410x10^{-4} \nu^2_{MHz}
#
# In this code we will adopt two approaches 
# one to fit a dispersion measure according to
# equation (1) and an other one that has a linear 
# relation of the form:
# 
# \tau = \alpha x \nu + \beta                (2)
#
# THe later will be easier to implement, and will 
# work faster, while the other one is more accurate.


def dispersionmeasure(nu,DM,A):
    ######################################
    # Function of the dispersion measure #
    ######################################
    # nu -> frequency in MHz
    # DM -> dispersion measure in cm^-3 pc
    # A -> arbitrary time displacement in seconds
    return DM/(2.41e-4*nu*nu) + A

def DMrand(nu,DMrand,A):
    ######################################
    # Function of the dispersion measure #
    # without units                      #
    ######################################
    # nu -> frequency in arbitrary unit
    # DM -> dispersion measure in arbitrary unit
    # A -> arbitrary time displacement in seconds
    return DMrand/(nu*nu) + A


# Find the maximum of everychannel
# This is seen as a first order estimate for the 
# peak of every pulse
maxchannel = np.argmax(normalisedfoldedarray,axis=0)

# calculate the frequencies of every channel
# not sure if this is correct (?????)
frequencies = 420. - 21.668359375 + 35.0*np.arange(256)/256.0

# only execute this part of the code if we want to look 
# the inverse square law version of the dispersion measure.
if inversesquare==True:
    # find the best fit parameters
    fitDM = sco.curve_fit(dispersionmeasure,frequencies[10:100],maxchannel[10:100],p0=[DM,1000])

    # the results of the maximum with fitted dispersion measure
    fitDMresult = dispersionmeasure(frequencies,fitDM[0][0],fitDM[0][1])

    plt.plot(frequencies,maxchannel)
    plt.plot(frequencies,fitDMresult)
    #plt.plot(frequencies,dispersionmeasure(frequencies,40000,1000))
    plt.savefig('first-estimate-dm.pdf')
    if interacticeplots==True:
        plt.show()
    plt.close()


    if bestfitDM==True:
        print('The best fit parameters for the DM and A are:')
        print(fitDM[0][0],fitDM[0][1])

    # calculate the residuals 
    residual = maxchannel-fitDMresult


    # calculate the elements that are fine
    fineresiduals = abs(residual)<.05*nbins

    # calculate an aproved
    fitDMimproved = sco.curve_fit(dispersionmeasure,frequencies[fineresiduals],maxchannel[fineresiduals],p0=[DM,1000])

    if bestfitDM==True:
        print('The improved best fit parameters for the DM and A are:')
        print(fitDMimproved[0][0],fitDMimproved[0][1])


    # improved fit result
    fitDMresultimproved = dispersionmeasure(frequencies,fitDMimproved[0][0],fitDMimproved[0][1])

    plt.plot(frequencies,maxchannel)
    plt.plot(frequencies,fitDMresultimproved)
    #plt.plot(frequencies,dispersionmeasure(frequencies,40000,1000))
    plt.savefig('second-estimate-dm.pdf')
    if interacticeplots==True:
        plt.show()
    plt.close()


###############################################


def linearfunc(x,a,b):
    ######################################
    # Function for the time delay        #
    ######################################
    return a*x + b

xpoints = np.arange(len(maxchannel))

if linearcase==True:
    linearfit = sco.curve_fit(linearfunc,xpoints[10:100],maxchannel[10:100],p0=[-10,1000])
    fitresult = linearfunc(xpoints,linearfit[0][0],linearfit[0][1])

    if bestfitDM==True:
        print('The best fit parameters for the a and b are:')
        print(linearfit[0][0],linearfit[0][1])

    plt.plot(xpoints,maxchannel)
    plt.plot(xpoints,fitresult)
    #plt.plot(frequencies,dispersionmeasure(frequencies,40000,1000))
    plt.savefig('linear1-estimate-dm.pdf')
    if interacticeplots==True:
        plt.show()
    plt.close()

    # calculate the residuals 
    residual = maxchannel-fitresult


    # calculate the elements that are fine
    fineresiduals = abs(residual)<.05*nbins

    # calculate an aproved
    fitDMimproved = sco.curve_fit(linearfunc,xpoints[fineresiduals],maxchannel[fineresiduals],p0=[DM,1000])

    if bestfitDM==True:
        print('The best fit parameters for the a and b are:')
        print(fitDMimproved[0][0],fitDMimproved[0][1])

    # improved fit result
    fitDMresultimproved = linearfunc(xpoints,fitDMimproved[0][0],fitDMimproved[0][1])

    plt.plot(xpoints,maxchannel)
    plt.plot(xpoints[fineresiduals],maxchannel[fineresiduals],'ro')
    plt.plot(xpoints,fitDMresultimproved)
    #plt.plot(frequencies,dispersionmeasure(frequencies,40000,1000))
    plt.savefig('linear2-estimate-dm.pdf')
    if interacticeplots==True:
        plt.show()
    plt.close()




    # calculate the shift with respect to the first element
    shift = fitDMresultimproved-fitDMresultimproved[0]

    # initialize an empty array for the pulse profile
    finalprofile = np.zeros(len(normalisedfoldedarray[:,0]))

    for i in range(len(maxchannel)):
        if fineresiduals[i]==True:
            #print(i)
            # calculate the current shift
            currentshift = shift[i]

            # calculate the index
            lowerindex = int(np.floor(currentshift))
            higherindex = lowerindex+1

            # calculate the weight
            higherweigth = currentshift - lowerindex
            lowerweigth = 1- higherweigth

            # load the current pulse profile
            currentprofile = normalisedfoldedarray[:,i]

            # print(np.roll(currentprofile,10))
            finalprofile += lowerweigth*np.roll(currentprofile,lowerindex) + higherweigth*np.roll(currentprofile,higherindex)


            #print(currentshift,lowerindex,higherindex,lowerweigth,higherweigth)


    plt.plot(finalprofile)
    plt.savefig('pulseprofile.pdf')
    if interacticeplots==True:
        plt.show()
    plt.close()

t2 = time.time()
if comptime==True:
    print('part 9 =',t2-t1)
    

###################################
# 9. De-dispersion ################
###################################
if DMROI == True:
#creating an array with the delays for dispersion and then an array with the shift in bins
    frequencyarray = np.linspace(0.399,0.44,255)
    #DM = 0
    timedelays = 4.15e-3*DM*(frequencyarray[0]**(-2)-frequencyarray**(-2))
    binshifts = np.round(timedelays/dt)
#Applying the dispersion meassure
    for i in range(len(normalisedfoldedarray[0,:])-1):
            normalisedfoldedarray[:,i+1] = np.roll(normalisedfoldedarray[:,i+1],int(binshifts[i]))

#Array for plotting the period
    periodtime = np.linspace(0,period,nbins)

#Summing for the final puls profile
    finalpulsprofile = np.sum(normalisedfoldedarray,axis=1)
#Plotting
    from matplotlib.pyplot import figure, show
    fig = figure(figsize=(20,10))
    frame = fig.add_subplot(1,1,1)
    frame.plot(periodtime,np.roll(finalpulsprofile,100))
    show()
    
    plt.matshow(np.log10(normalisedfoldedarray))
    plt.savefig('dedispersed.png') 
    plt.show()
    plt.close()
    
    
    
