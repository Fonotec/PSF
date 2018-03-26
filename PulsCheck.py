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

DMplay = True

# Create an object containing all useful pulsar properties
obs = Observation(args.datafile)
pulsar = obs.pulsar
twodarray = obs.data

# read the literature value of the period and the dispersion measure
period = pulsar.period
DM = pulsar.DM

# Time resolution of the telescope
dt = (512*64)/(70e6)

tens = 10*int(np.round(1/dt))
thirs = int(3*tens)
sixts = int(6*tens)

# Array with the bandwith
frequencyarray = obs.freq

# Create 3 different observing times to fold

twodarray10 = twodarray[:tens,:]
twodarray30 = twodarray[:thirs,:]
twodarray60 = twodarray[:sixts,:]


# calculate the folded arrays
foldedarray10 = timeFolding(twodarray10, args.nbins, period, corrected_times=obs.times)
foldedarray30 = timeFolding(twodarray30, args.nbins, period, corrected_times=obs.times)
foldedarray60 = timeFolding(twodarray60, args.nbins, period, corrected_times=obs.times)
foldedarray   = timeFolding(twodarray, args.nbins, period, corrected_times=obs.times)

#show the rainfall plot and allow for fiddling with the DM

DM = 8.5

print(DM)
waterfall(dedispersion(foldedarray,DM,frequencyarray))


if DMplay:
	DM2 = DM	
	while True:
		disp = foldedarray[:]
		DM1 = input("Input new DM:")
		if DM1 == "":
			DM = float(DM2)
			break
		waterfall(dedispersion(disp,float(DM1),frequencyarray))
		DM2 = float(DM1)

fin10 = pulseProfile(foldedarray10,DM,frequencyarray)
fin30 = pulseProfile(foldedarray30,DM,frequencyarray)
fin60 = pulseProfile(foldedarray60,DM,frequencyarray)
fin   = pulseProfile(foldedarray  ,DM,frequencyarray)

fig = plt.figure(figsize=(20,20))
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)

ax1.plot(fin10)
ax1.set_title("10 seconds")
ax2.plot(fin30)
ax2.set_title("30 seconds")
ax3.plot(fin60)
ax3.set_title("60 seconds")
ax4.plot(fin)
ax4.set_title("full")

plt.show()
	

	
	




