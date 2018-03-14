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
from pulsarsObjects import Pulsar, load_pulsar_data
from loadData import loader
from folding import timeFolding
from plotTools import waterfall
from flagging import flagData
from dispersionMeasure import dedispersion, pulseProfile, fitDM, DMfunction
from barcen import barcen_times
from observation import Observation

startScreen('1.1.0')


parser = argparse.ArgumentParser(description='Pulsar folding!')
parser.add_argument('-d', '--datafile', default='/net/dataserver2/data/users/nobels/CAMRAS/obs-10-04-2018/B0329+54_10-04-2018.fits', help='The location of the *.fits file.')
parser.add_argument('-b','--nbins', default=500, type=int, help='The number of phase bins to fold with. Higher means higher time resolution, but noisier folds.')
parser.add_argument('-p','--pulsarcat', default='./pulsarcat.csv', help='The csv file containing pulsar data')
args = parser.parse_args()

# Create an object containing all useful pulsar properties
obs = Observation(args.datafile)
pulsar = obs.pulsar
twodarray = obs.data

# read the literature value of the period and the dispersion measure
period = pulsar.period
DM = pulsar.DM

# Time resolution of the telescope
dt = (512*64)/(70e6)

# Array with the bandwith
frequencyarray = obs.freq

# this part should be RFI flagging something like:
# noflag = flagging(twodarray)

flag=flagData(twodarray)

# calculate the folded array
foldedarray = timeFolding(twodarray, args.nbins, period, flagged = flag, corrected_times=obs.times)

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

plt.plot(frequencyarray,maximum)
plt.plot(frequencyarray,DMfunction(frequencyarray,fitres[0][0],fitres[0][1],fitres[0][2]))
plt.show()
