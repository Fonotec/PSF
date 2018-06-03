#!/usr/bin/env python
import socket
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

from observation import Observation
from time import sleep


live = False

data = np.zeros(512,dtype=int)

if live:

    DM = 24.5
    period = 0.71458
    # define data type unsigned int
    unsignint = np.dtype(np.uint32)

    # construct the socekt
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # get socket info
    sinfo = socket.getaddrinfo('0.0.0.0',22102)

    # bind with the backend
    s.bind(('0.0.0.0',22102))
    #s.connect(('10.1.2.3',22102))

    # receive one package
    a = s.recv(2048)
else:
    obs = Observation("data/obs-10-04-2018/B0329+54_10-04-2018-withP.fits.gz")

    DM = obs.pulsar.DM
    period=0.71458


# define a counter 
counter = 0
# how many modulus of counters do we want.
countmod = 10
nbins = 500

# construct a figure
fig, [ax,axfold] = plt.subplots(2,1)
plt.show(False)
ax.set_ylim(125,140)
ax.set_xlim(0,400)
axfold.set_ylim(1/nbins*0.96, 1/nbins*1.1)
axfold.set_xlim(0,nbins)
plt.draw()
background = fig.canvas.copy_from_bbox(ax.bbox)
background_fold = fig.canvas.copy_from_bbox(axfold.bbox)

# define the x points and construct a plot
#xpoints = range(len(np.log10(data)[256:]))
plotarray = np.ones(1000)
xpoints = np.arange(len(plotarray))
points = ax.plot(xpoints,plotarray)[0]
points_folded = axfold.plot(np.ones(nbins))[0]

dt = 512*64/70e6

def calc_freqs(mix_freq):
    timevoltage = 1/(70e6) # (s), the time of each voltage measurement
    timefft = 512*timevoltage # (s), the time of each fft block: of each 512 voltage measurements an fft is taken
    dt = timefft * 64 # (s), to reduce the data rate, the sum of 64 ffts is taken
    freqstep = (1/timefft)/1e6 # (MHz), the bandwidth of each frequency bin

    maxfreq = (mix_freq+21.4) # (MHz)
    minfreq = maxfreq-35 # (MHz)

    freqs_edges = np.linspace(minfreq, maxfreq, 257) # Frequency bin edges
    freqs = (freqs_edges[1:]+freqs_edges[:-1])/2 # Frequency bin centers
    return freqs

mixfreq=405
freq = calc_freqs(mixfreq)[1:]

shift = 4.15e3*DM*(1/freq[0]**2 - 1/freq**2)
#binshifts = np.zeros(len(shift),dtype=int)
binshifts = np.rint(shift/dt).astype(int)

sizet = binshifts[-1]
dmdata = np.zeros((sizet,len(shift)))
maxshift = binshifts[-1]

plotarray = np.ones(1000)
xpoints = np.arange(len(plotarray))

newdatapoint = 0

normdata = np.zeros((20000,255)) ## 256->255
for j in range(0,20000):
    if live:
        # get the package of the current time
        a = s.recv(2048)
        # save the data in the array
        for i in range(1,512):
            data[i-1] = int.from_bytes(a[4*(i-1):4*i],byteorder='big')
        #print(len(normdata[j]),len(data[256:]))
        normdata[j] = data[256:]
    else:
        normdata[j] = obs.data[j]

norm = np.sum(normdata, axis = 0)/20000


# construct the most ugly while loop construction
foldedarray = np.zeros(nbins)
normalarray = np.zeros(nbins)
while True:
    if live:
        # get the package of the current time
        a = s.recv(2048)
        
        # save the data in the array
        for i in range(1,512):
            data[i-1] = int.from_bytes(a[4*(i-1):4*i],byteorder='big')

        localdata = data[256:]
    else:
        localdata = obs.data[counter]

    time = counter*dt
    delay_dispersion = -4.148e3*DM*freq**(-2)
    time += delay_dispersion
    whichbin = time*nbins/period % nbins

    lowernorm = np.ceil(whichbin)-whichbin
    highernorm = 1-lowernorm
    indexlow = np.array(np.floor(whichbin), dtype=int)
    indexhigh = (indexlow + 1) % nbins
    
    np.add.at(normalarray, indexlow, lowernorm)
    np.add.at(normalarray, indexhigh, highernorm)
    np.add.at(foldedarray, indexlow, lowernorm*localdata/norm)
    np.add.at(foldedarray, indexhigh, highernorm*localdata/norm)
    
    for i in range(0,len(shift)-1):
        dmdata[(counter+binshifts[i])%maxshift,i] = localdata[i]/norm[i]
        if norm[i] == 0:
            print('Hellppp!',i)
    
    newdatapoint += np.sum(dmdata[counter%maxshift,70:200])
    
    # if the current time is a plot time, plot
    if counter%countmod==0:
        plotarray = np.roll(plotarray,1)
        plotarray[0] = newdatapoint/countmod
        # plot the current time normalized
        points.set_data(xpoints,plotarray)
        to_plot = foldedarray/normalarray
        points_folded.set_data(np.arange(len(to_plot)),to_plot/to_plot.sum())
        fig.canvas.restore_region(background)
        fig.canvas.restore_region(background_fold)
        ax.draw_artist(points)
        axfold.draw_artist(points_folded)
        fig.canvas.blit(ax.bbox)
        fig.canvas.blit(axfold.bbox)
        
        newdatapoint = 0
        
    counter += 1

plt.close(fig)






