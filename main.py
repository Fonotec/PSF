#!/usr/bin/env python
# coding: utf-8
# importing all the used modules
import numpy as np
import math as ma
import time
import matplotlib.pyplot as plt
import scipy as sc
import scipy.optimize as sco
import sys
from startscreen import startScreen
from pulsarsObjects import Pulsar
from loadData import loader
from folding import timeFolding
from plotTools import waterfall


startScreen('1.1.0')

# read the data of the pulsar database
pulsardata = np.genfromtxt('pulsardata.txt', dtype=None)

# construct a list to add pulsar object to it
pulsarlist = []

# construct all the pulsar objects
for i in range(0,len(pulsardata)):
    currentpulsar = pulsardata[i]
    pulsarlist.append(Pulsar(currentpulsar))

# Specify your pulsar
pulsarname = 'B0329+54'

pulsar = 'None'
# search for the correct pulsar
for i in range(0,len(pulsarlist)):
    if pulsarlist[i].getName == pulsarname:
        pulsar = pulsarlist[i]

# check if we actually found the pulsar in the data base
if pulsar=='None':
    print('Your defined pulsar is not found in the database')
    print('Program exits with an ERROR!!')
    exit(0)

# read the literature value of the period and the dispersion measure
period = pulsar.period
DM = pulsar.DM

# Time resolution of the telescope
dt = (512*64)/(70e6)

# Array with the bandwith
frequencyarray = np.linspace(0.402,0.433,255)

# load the data
twodarray = loader('B0329 54.2016.11.18.1038.5min.dat')


# part for folding
# Number of bins per period
nbins = int(round(period/dt))

# Stepsize in units of bin
stepsize = dt*nbins/period

# this part should be RFI flagging something like:
# noflag = flagging(twodarray)

noflag=twodarray[:,0]>0
# for the moment lets make everything not flagged

foldedarray = timeFolding(twodarray,nbins,stepsize,noflag)

waterfall(foldedarray)



