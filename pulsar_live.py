#!/usr/bin/env python
import socket
import numpy as np
import matplotlib

matplotlib.use("tkagg")
import matplotlib.pyplot as plt
import ctypes
from time import sleep, time_ns
import multiprocessing as mp

from observation import Observation

dt = 512 * 64 / 70e6


live = False  # Live? Or just testing?
countmod = 10  # Once per how many packets should the to-plot array be updated?
nbins = 500  # How many bins are to be used for folding?
nlive = 1000  # How many points to plot the live version of?
mixfreq = 403.975  # The default...
nframesinit = int(1 / dt)  # How long to collect normalization data

MTU = 8900


def mp2np(mp_array):
    return np.frombuffer(mp_array.get_obj())


def calc_freqs(mix_freq):
    timevoltage = 1 / (70e6)  # (s), the time of each voltage measurement
    timefft = (
        512 * timevoltage
    )  # (s), the time of each fft block: of each 512 voltage measurements an fft is taken
    dt = timefft * 64  # (s), to reduce the data rate, the sum of 64 ffts is taken
    freqstep = (1 / timefft) / 1e6  # (MHz), the bandwidth of each frequency bin

    maxfreq = mix_freq + 21.4  # (MHz)
    minfreq = maxfreq - 35  # (MHz)

    freqs_edges = np.linspace(minfreq, maxfreq, 257)  # Frequency bin edges
    freqs = (freqs_edges[1:] + freqs_edges[:-1]) / 2  # Frequency bin centers
    return freqs


def data_worker(pipe):
    # Waits for the telescope to send some new data and sends it to some pipe
    counter = 0
    pd_output, p_input = pipe
    data = np.zeros(512, dtype=int)
    packet_counter = None

    while True:
        if live:
            # get the package of the current time
            a = s.recv(MTU)

            # save the data in the array
            for i in range(1, 512):
                data[i - 1] = int.from_bytes(a[4 * (i - 1) : 4 * i], byteorder="big")

            if data[0] - 1 != packet_counter and packet_counter is not None:
                print(f"Missed {data[0]-packet_counter} packets at {packet_counter}")
            packet_counter = data[0]

            localdata = data[
                257:
            ]  # Throwing lowest freq bin away here. Mostly for convenience, because this way it is consistent with the offline files.
        else:
            localdata = obs.data[counter]
            counter += 1
            sleep(1e-4)

        p_input.send(localdata)


def fold_worker(pipe_data, livearray, folded_fullynormed):
    # Processes the current data packets and does all the folding.
    # Updates the arrays containing the data for the plots
    pd_output, pd_input = pipe_data
    pd_input.close()

    newdatapoint = 0
    counter = 0

    freq_norms = np.zeros(255)
    for i in range(nframesinit):
        freq_norms += pd_output.recv(MTU)

    print(freq_norms, freq_norms.min(), freq_norms.shape)

    foldedarray_notnormed = np.zeros(nbins)
    folding_norms = np.zeros(nbins)
    while True:
        tnow = time_ns() / 1e6
        localdata = pd_output.recv(MTU)
        print(time_ns() / 1e6 - tnow)
        counter += 1
        time = counter * dt
        delay_dispersion = -4.148e3 * DM * freq ** (-2)
        time += delay_dispersion
        whichbin = time * nbins / period % nbins

        lowernorm = np.ceil(whichbin) - whichbin
        highernorm = 1 - lowernorm
        indexlow = np.array(np.floor(whichbin), dtype=int)
        indexhigh = (indexlow + 1) % nbins

        # freq_norms += localdata # Maybe this'd be good?
        np.add.at(folding_norms, indexlow, lowernorm)
        np.add.at(folding_norms, indexhigh, highernorm)
        np.add.at(foldedarray_notnormed, indexlow, lowernorm * localdata / freq_norms)
        np.add.at(foldedarray_notnormed, indexhigh, highernorm * localdata / freq_norms)

        for i in range(0, len(shift) - 1):
            dmdata[(counter + binshifts[i]) % maxshift, i] = (
                localdata[i] / freq_norms[i]
            )
            if freq_norms[i] == 0:
                print("Hellppp!", i)

        newdatapoint += np.sum(dmdata[counter % maxshift, 70:200])

        # if the current time is a plot time, update the relevant arrays
        if counter % countmod == 0:
            with folded_fullynormed.get_lock():
                ffn = mp2np(folded_fullynormed)
                ffn[:] = foldedarray_notnormed / folding_norms
            with livearray.get_lock():
                livearraynp = mp2np(livearray)
                livearraynp[:] = np.roll(livearraynp, 1)
                livearraynp[0] = newdatapoint / countmod
                newdatapoint = 0


def plot_worker(tp_live, tp_folded):
    # construct a figure
    fig, [ax, axfold] = plt.subplots(2, 1)
    plt.show(False)
    ax.set_ylim(0.05, 0.08)
    ax.set_xlim(0, nlive)
    axfold.set_ylim(1 / nbins * 0.96, 1 / nbins * 1.1)
    axfold.set_xlim(0, nbins)
    fig.canvas.draw()
    background = fig.canvas.copy_from_bbox(ax.bbox)
    background_fold = fig.canvas.copy_from_bbox(axfold.bbox)

    # define the x points and construct a plot
    # xpoints = range(len(np.log10(data)[256:]))
    x_live = np.arange(nlive)
    x_folded = np.arange(nbins)
    points = ax.plot(x_live, np.ones(nlive) * 0.06)[0]
    points_folded = axfold.plot(x_folded, np.ones(nbins))[0]
    while True:
        # print(mp2np(tp_folded)[:5])
        # print(mp2np(tp_live))
        # plot the current time normalized
        y_live = mp2np(tp_live)
        points.set_data(x_live, y_live)
        y_folded = mp2np(tp_folded)
        points_folded.set_data(x_folded, y_folded / y_folded.sum())

        fig.canvas.restore_region(background)
        fig.canvas.restore_region(background_fold)
        ax.draw_artist(points)
        axfold.draw_artist(points_folded)
        fig.canvas.blit(ax.bbox)
        fig.canvas.blit(axfold.bbox)

    plt.close(fig)


if __name__ == "__main__":
    if live:
        pulsar = Pulsar(pulsarname="B0329+54")
        DM = pulsar.DM
        period = pulsar.apparent_period()

        s = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, proto=socket.PROTOIP_UDP
        )  # construct the socket
        s.setsockopt(
            socket.SOL_SOCKET, socket.SO_RCVBUF, (8 * 1024 * 1024)
        )  # May need tweaking.
        sinfo = socket.getaddrinfo("0.0.0.0", 22102)  # get socket info
        s.bind(("0.0.0.0", 22102))  # bind with the backend
        # s.connect(('10.1.2.3',22102))
        a = s.recv(MTU)  # Test it; receive one package
    else:
        obs = Observation("data/obs-10-04-2018/B0329+54_10-04-2018-withP.fits.gz")
        DM = obs.pulsar.DM
        period = obs.pulsar.apparent_period(tobs=obs.obs_middle)

    freq = calc_freqs(mixfreq)[1:]

    shift = 4.148e3 * DM * (1 / freq[0] ** 2 - 1 / freq ** 2)
    binshifts = np.rint(shift / dt).astype(int)

    sizet = binshifts[-1]
    dmdata = np.zeros((sizet, len(shift)))
    maxshift = binshifts[-1]

    data_pipe = mp.Pipe()
    folded_fnormed = mp.Array(ctypes.c_double, nbins)
    live_data = mp.Array(ctypes.c_double, nlive)

    data_proc = mp.Process(target=data_worker, args=(data_pipe,), daemon=True)
    fold_proc = mp.Process(
        target=fold_worker, args=(data_pipe, live_data, folded_fnormed), daemon=True
    )
    data_proc.start()
    fold_proc.start()

    plot_worker(live_data, folded_fnormed)
