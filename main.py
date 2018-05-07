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
from dispersionMeasure import dedispersion
from barcen import barcen_times
from observation import Observation

startScreen('1.1.0')


parser = argparse.ArgumentParser(description='Pulsar folding!')
parser.add_argument('-d', '--datafile', default='/net/dataserver2/data/users/nobels/CAMRAS/obs-10-04-2018/B0329+54_10-04-2018.fits', help='The location of the *.fits file.')
parser.add_argument('--nbins', default=500, type=int, help='The number of phase bins to fold with. Higher means higher time resolution, but noisier waterfalls.')
parser.add_argument('--nbinsdedisp', default=500, type=int, help='The number bins to show the dedispersed profile with. Higher means higher time resolution, but noisier folds.')
parser.add_argument('-p','--pulsarcat', default='./small-data-files/pulsarcat.csv', help='The csv file containing pulsar data')
parser.add_argument('--skiprfi', action='store_true', help='Use this to skip time-based rfi-peak removal.')
args = parser.parse_args()

# Create an object containing all useful pulsar properties
print("Loading data")
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

print("Flagging bad data")
flag = obs.data == 0 if args.skiprfi else flagData(twodarray)
obs.flag = flag

print("Folding")
# calculate the folded array
foldedarray = timeFolding(twodarray, args.nbins, period, flagged = flag, corrected_times=obs.times)

# make a waterfall plot of the result
waterfall(foldedarray)

print("Dedispersing")
# do the dedispersion
pulse_profile = dedispersion(foldedarray, obs, period, obs.pulsar.DM, freq_fold_bins=args.nbinsdedisp)

# plot the final pulse profile
plt.plot(pulse_profile)
plt.show()
