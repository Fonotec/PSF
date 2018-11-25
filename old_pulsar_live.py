#!/usr/bin/env python
import socket
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("TKAgg")

from observation import Observation
from time import sleep

obs = Observation("data/obs-10-04-2018/B0329+54_10-04-2018-withP.fits.gz")

DM = 26.8

# define data type unsigned int
## unsignint = np.dtype(np.uint32)

# construct the socekt
## s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# get socket info
## sinfo = socket.getaddrinfo('0.0.0.0',22102)

# bind with the backend
## s.bind(('0.0.0.0',22102))
# s.connect(('10.1.2.3',22102))
data = np.zeros(512, dtype=int)

# receive one package
## a = s.recv(2048)

# define a counter
counter = 0
# how many modulus of counters do we want.
countmod = 10

# construct a figure
fig, ax = plt.subplots(1, 1)
plt.show(False)
plt.ylim(125, 140)
plt.xlim(0, 400)
plt.draw()
background = fig.canvas.copy_from_bbox(ax.bbox)

# define the x points and construct a plot
# xpoints = range(len(np.log10(data)[256:]))
plotarray = np.ones(1000)
xpoints = np.arange(len(plotarray))
points = ax.plot(xpoints, plotarray)[0]

timevoltage = 1 / (70e6)  # (s), the time of each voltage measurement
timefft = (
    512 * timevoltage
)  # (s), the time of each fft block: of each 512 voltage measurements an fft is taken
dt = timefft * 64  # (s), to reduce the data rate, the sum of 64 ffts is taken
freqstep = (1 / timefft) / 1e6  # (MHz), the bandwidth of each frequency bin

midfreq = 405
maxfreq = midfreq + 21.4  # (MHz)
minfreq = maxfreq - 35  # (MHz)

freqs_edges = np.linspace(minfreq, maxfreq, 257)  # Frequency bin edges
freqs = (freqs_edges[1:] + freqs_edges[:-1]) / 2


shift = 4.15e3 * DM * (1 / freqs[0] ** 2 - 1 / freqs ** 2)
# binshifts = np.zeros(len(shift),dtype=int)
binshifts = np.rint(shift / dt).astype(int)

sizet = binshifts[-1]
dmdata = np.zeros((sizet, len(shift)))
maxshift = binshifts[-1]

plotarray = np.ones(1000)
xpoints = np.arange(len(plotarray))

newdatapoint = 0

normdata = np.zeros((20000, 255))  ## 256->255
for j in range(0, 20000):
    # get the package of the current time
    # a = s.recv(2048)
    # save the data in the array
    # for i in range(1,512):
    # data[i-1] = int.from_bytes(a[4*(i-1):4*i],byteorder='big')
    # print(len(normdata[j]),len(data[256:]))
    normdata[j] = obs.data[j]

norm = np.sum(normdata, axis=0) / 20000
print(norm)


# construct the most ugly while loop construction
t = 0
while True:
    # get the package of the current time
    ## a = s.recv(2048)

    # save the data in the array
    ## for i in range(1,512):
    ## data[i-1] = int.from_bytes(a[4*(i-1):4*i],byteorder='big')

    ## localdata = data[256:]
    localdata = obs.data[t]
    t += 1

    for i in range(0, len(shift) - 1):
        dmdata[(counter + binshifts[i]) % maxshift, i] = localdata[i] / norm[i]
        if norm[i] == 0:
            print("Hellppp!", i)

    newdatapoint += np.sum(dmdata[counter % maxshift, 70:200])

    # if the current time is a plot time, plot
    if counter % countmod == 0:
        plotarray = np.roll(plotarray, 1)
        plotarray[0] = newdatapoint / countmod
        # plot the current time normalized
        points.set_data(xpoints, plotarray)
        fig.canvas.restore_region(background)
        ax.draw_artist(points)
        fig.canvas.blit(ax.bbox)
        # print(counter)
        print(newdatapoint)

        newdatapoint = 0

    counter += 1

plt.close(fig)
