#!/usr/bin/env python
import socket
import numpy as np
import matplotlib

matplotlib.use("TKAgg")
import matplotlib.pyplot as plt

from observation import Observation, calc_central_freqs
from time import sleep

import multiprocessing
import ctypes

dt = 512 * 64 / 70e6


def calc_worker(
    DM,
    period,
    live_x,
    live_y,
    folded_x,
    folded_y,
    live=False,
    nbins=500,
    countmod=10,
    mixfreq=405,
):
    """
    nbins: number of bins to plot
    countmod: after how many new data points to update the plot-array
    """
    data = np.zeros(512, dtype=int)

    if live:
        # define data type unsigned int
        unsignint = np.dtype(np.uint32)

        # construct the socekt
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # get socket info
        sinfo = socket.getaddrinfo("0.0.0.0", 22102)

        # bind with the backend
        s.bind(("0.0.0.0", 22102))
        # s.connect(('10.1.2.3',22102))

        # receive one package
        a = s.recv(2048)
    else:
        obs = Observation("data/obs-10-04-2018/B0329+54_10-04-2018-withP.fits.gz")

        DM = obs.pulsar.DM
        period = 0.71458

    # define a counter
    counter = 0
    # how many modulus of counters do we want.

    freq = calc_central_freqs(mixfreq, throwhighestfreqaway=(False if live else True))
    num_freqs = len(freq)

    shift = 4.148e3 * DM * (1 / freq[0] ** 2 - 1 / freq ** 2)
    # binshifts = np.zeros(len(shift),dtype=int)
    binshifts = np.rint(shift / dt).astype(int)

    sizet = binshifts[-1]
    dmdata = np.zeros((sizet, len(shift)))
    maxshift = binshifts[-1]

    plotarray = np.ones(1000)
    xpoints = np.arange(len(plotarray))

    newdatapoint = 0

    normdata = np.zeros((20000, num_freqs))
    for j in range(0, 20000):
        if live:
            # get the package of the current time
            a = s.recv(2048)
            # save the data in the array
            for i in range(1, 512):
                data[i - 1] = int.from_bytes(a[4 * (i - 1) : 4 * i], byteorder="big")
            # print(len(normdata[j]),len(data[256:]))
            normdata[j] = data[256:]
        else:
            normdata[j] = obs.data[j]

    norm = np.sum(normdata, axis=0) / 20000

    # construct the most ugly while loop construction
    foldedarray = np.zeros(nbins)
    normalarray = np.zeros(nbins)
    while True:
        if live:
            # get the package of the current time
            a = s.recv(2048)

            # save the data in the array
            for i in range(1, 512):
                data[i - 1] = int.from_bytes(a[4 * (i - 1) : 4 * i], byteorder="big")

            localdata = data[256:]
        else:
            localdata = obs.data[counter]

        time = counter * dt
        delay_dispersion = -4.148e3 * DM * freq ** (-2)
        time += delay_dispersion
        whichbin = time * nbins / period % nbins

        lowernorm = np.ceil(whichbin) - whichbin
        highernorm = 1 - lowernorm
        indexlow = np.array(np.floor(whichbin), dtype=int)
        indexhigh = (indexlow + 1) % nbins

        np.add.at(normalarray, indexlow, lowernorm)
        np.add.at(normalarray, indexhigh, highernorm)
        np.add.at(foldedarray, indexlow, lowernorm * localdata / norm)
        np.add.at(foldedarray, indexhigh, highernorm * localdata / norm)

        for i in range(0, len(shift) - 1):
            dmdata[(counter + binshifts[i]) % maxshift, i] = localdata[i] / norm[i]
            if norm[i] == 0:
                print("Hellppp!", i)

        newdatapoint += np.sum(dmdata[counter % maxshift, 70:200])

        # if the current time is a plot time, plot
        if counter % countmod == 0:
            plotarray = np.roll(plotarray, -1)
            plotarray[-1] = newdatapoint / countmod
            to_plot = foldedarray / normalarray
            live_x[:] = np.linspace(-countmod * 1000 * dt, 0, 1000)
            live_y[:] = plotarray
            folded_x[:] = np.linspace(0, period, nbins, endpoint=False)
            folded_y[:] = to_plot / to_plot.sum()

            newdatapoint = 0

        counter += 1


def plot_worker(
    period, lookbacktime, live_x, live_y, folded_x, folded_y, to_plotnbins=500
):
    # construct a figure
    fig, [ax, axfold] = plt.subplots(2, 1)
    plt.show(False)
    ax.set_ylim(125, 140)
    ax.set_xlim(-lookbacktime, 0)
    axfold.set_ylim(1 / nbins * 0.96, 1 / nbins * 1.1)
    axfold.set_xlim(0, period)
    plt.draw()
    background = fig.canvas.copy_from_bbox(ax.bbox)
    background_fold = fig.canvas.copy_from_bbox(axfold.bbox)

    plotarray = np.ones(1000)
    points = ax.plot(live_x, live_y)[0]
    points_folded = axfold.plot(folded_x, folded_y)[0]
    while True:
        points.set_data(live_x, live_y)
        points_folded.set_data(folded_x, folded_y)
        fig.canvas.restore_region(background)
        fig.canvas.restore_region(background_fold)
        ax.draw_artist(points)
        axfold.draw_artist(points_folded)
        fig.canvas.blit(ax.bbox)
        fig.canvas.blit(axfold.bbox)


if __name__ == "__main__":
    nbins = 500
    nlive = 1000
    SA_base_foldedx = multiprocessing.Array(ctypes.c_double, nbins)
    SA_foldedx = np.ctypeslib.as_array(SA_base_foldedx.get_obj())
    SA_base_foldedy = multiprocessing.Array(ctypes.c_double, nbins)
    SA_foldedy = np.ctypeslib.as_array(SA_base_foldedy.get_obj())

    SA_base_livex = multiprocessing.Array(ctypes.c_double, nlive)
    SA_livex = np.ctypeslib.as_array(SA_base_livex.get_obj())
    SA_base_livey = multiprocessing.Array(ctypes.c_double, nlive)
    SA_livey = np.ctypeslib.as_array(SA_base_livey.get_obj())

    p_calc = multiprocessing.Process(
        target=calc_worker,
        args=(0.71458, 0, SA_livex, SA_livey, SA_foldedx, SA_foldedy),
    )
    p_calc.start()

    #    p_plot = multiprocessing.Process(target=plot_worker, args=(SA_livex, SA_livey, SA_foldedx, SA_foldedy))
    #    p_plot.start()
    #    p_plot.join()

    plot_worker(0.71458, 10 * 1000 * dt, SA_livex, SA_livey, SA_foldedx, SA_foldedy)
    p_calc.join()
