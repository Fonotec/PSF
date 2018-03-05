#!/usr/bin/env python
# coding: utf-8
# importing all the used modules
import numpy as np
import math as ma
import time
import matplotlib.pyplot as plt
import scipy as sc
import scipy.optimize as sco
import argparse
from startscreen import startScreen
from pulsarsObjects import Pulsar
from loadData import loader
from folding import timeFolding
from plotTools import waterfall
from flagging import flagData
from dispersionMeasure import dedispersion, pulseProfile, fitDM, DMfunction

startScreen('1.1.0')


parser = argparse.ArgumentParser(description='Pulsar folding!')
parser.add_argument('-d', '--datafile', default='/net/dataserver2/data/users/nobels/CAMRAS/B0329 54.2016.11.18.1038.5min.dat', help='The location of the *.raw or *.dat data file.')
parser.add_argument('--pulsarname', default='B0329+54', help='The name of the pulsar, as noted in the database, \'pulsardata.txt\'.')
parser.add_argument('-b','--nbins', default=200, help='The number of phase bins to fold with. Higher means higher time resolution, but noisier folds.')
args = parser.parse_args()



# read the data of the pulsar database
pulsardata = np.genfromtxt('pulsardata.txt', dtype=None)

# construct a list to add pulsar object to it
pulsarlist = []

# construct all the pulsar objects
for i in range(0,len(pulsardata)):
    currentpulsar = pulsardata[i]
    pulsarlist.append(Pulsar(currentpulsar))

# Specify your pulsar
pulsarname = args.pulsarname

pulsar = None
# search for the correct pulsar
for i in range(0,len(pulsarlist)):
    if pulsarlist[i].getName == pulsarname:
        pulsar = pulsarlist[i]

# check if we actually found the pulsar in the data base
if pulsar is None:
    print('Your defined pulsar is not found in the database')
    print('Program exits with an ERROR!!')
    exit(1)

# read the literature value of the period and the dispersion measure
period = pulsar.period
DM = pulsar.DM

print(period)
# Time resolution of the telescope
dt = (512*64)/(70e6)

# Array with the bandwith
frequencyarray = np.linspace(0.402,0.433,255)*1e3
#frequencyarray = np.linspace(0.399,0.44,255)

# load the data
twodarray = loader(args.datafile)


# part for folding
# Number of bins per period
nbins = int(round(period/dt))

# Stepsize in units of bin
stepsize = dt*nbins/period

# this part should be RFI flagging something like:
# noflag = flagging(twodarray)

noflag=~flagData(twodarray)
# for the moment lets make everything not flagged, if this function is changed it will 
# be easy to extend on this

# calculate the folded array
foldedarray = timeFolding(twodarray, args.nbins, period, noflag)

# make a waterfall plot of the result
#waterfall(foldedarray)

# do the dedispersion

waterfall(dedispersion(foldedarray,DM,frequencyarray))

# plot the final pulse profile
plt.plot(pulseProfile(foldedarray,DM,frequencyarray))
plt.show()

#fitDM(foldedarray,frequencyarray)

maximum, fitres = fitDM(foldedarray,frequencyarray)

print(fitres)

plt.plot(frequencyarray,maximum[1:])
plt.plot(frequencyarray,DMfunction(frequencyarray,fitres[0][0],fitres[0][1],fitres[0][2]))
plt.show()
