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



# read the data of the file
pulsardata = np.genfromtxt('pulsardata.txt', dtype=None)

pulsarlist = []

for i in range(0,len(pulsardata)):
    currentpulsar = pulsardata[i]
    pulsarlist.append(Pulsar(currentpulsar))

print(pulsarlist[1].getName)
