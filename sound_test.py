#!/usr/bin/env python
import numpy as np
import pygame as pg
import scipy.interpolate as sci
import matplotlib.pyplot as plt

duration = 15.0  # in seconds
sample_rate = int(44100)
bits = 16
frequency_l = 400
frequency_r = 400

normal = False
Folkert = False
Reinier = False
Ewoud = False
ultra = True
ultra2 = True

folded = np.load("data/folded_Huys.npy")
folded = folded - np.min(folded)
folded /= np.max(folded)
folded[:, 140:] = 0
folded[:, :61] = 0


print(len(folded), len(folded[:, 0]), len(folded[0, :]))

nu = np.linspace(405 + 21.4 - 35, 405 + 21.4, 257)
nu = (nu[1:] + nu[:-1]) / 2
nu = nu[:-1]

time = np.linspace(0, 0.745, len(folded)) / 40

folded[folded < 0.6] = 0

f = sci.interp2d(nu, time, folded, kind="linear")

# plt.imshow(folded)
# plt.show()

nufake = nu - nu.min()
nufake /= nufake.max()
nufake *= 2
nufake = 10 ** nufake
nufake *= 100


def gauss(x, d, mu):
    return np.exp(-(x - mu) ** 2 / (2 * d ** 2))


try:
    pg.mixer.init(frequency=sample_rate, size=-bits, channels=2)
    Nsamples = int(round(duration * sample_rate))

    zeros = np.zeros((Nsamples, 2), dtype=np.int16)
    max_sample = 2 ** (bits - 1) - 1
    print(max_sample)
    for s in range(Nsamples):
        t = float(s) / sample_rate  # time in seconds
        # left box
        if normal:
            zeros[s][0] = int(round(max_sample * np.sin(2 * np.pi * frequency_l * t)))
            zeros[s][1] = int(round(max_sample * np.sin(2 * np.pi * frequency_r * t)))
        elif Folkert:
            zeros[s][0] = int(
                round(
                    max_sample
                    * np.sin(2 * np.pi * frequency_l * t)
                    * gauss(t, 0.1, 0.5)
                )
            )
            zeros[s][1] = int(
                round(
                    max_sample
                    * np.sin(2 * np.pi * frequency_r * t)
                    * gauss(t, 0.1, 0.5)
                )
            )
        elif Reinier:
            zeros[s][0] = int(
                round(
                    max_sample
                    * np.sin(2 * np.pi * frequency_l * (1 + gauss(t, 0.1, 0.5)) * t)
                )
            )
            zeros[s][1] = int(
                round(
                    max_sample
                    * np.sin(2 * np.pi * frequency_r * (1 + gauss(t, 0.1, 0.5)) * t)
                )
            )
        elif Ewoud:
            A = max_sample / 5
            zeros[s][0] = int(
                round(
                    A * np.sin(2 * np.pi * frequency_l * t * 0.8) * gauss(t, 0.1, 0.3)
                    + A * np.sin(2 * np.pi * frequency_l * t * 0.9) * gauss(t, 0.1, 0.4)
                    + A * np.sin(2 * np.pi * frequency_l * t) * gauss(t, 0.1, 0.5)
                    + A * np.sin(2 * np.pi * frequency_l * t * 1.1) * gauss(t, 0.1, 0.6)
                    + A * np.sin(2 * np.pi * frequency_l * t * 1.2) * gauss(t, 0.1, 0.7)
                )
            )
            zeros[s][1] = int(
                round(
                    A * np.sin(2 * np.pi * frequency_r * t * 0.8) * gauss(t, 0.1, 0.3)
                    + A * np.sin(2 * np.pi * frequency_r * t * 0.9) * gauss(t, 0.1, 0.4)
                    + A * np.sin(2 * np.pi * frequency_r * t) * gauss(t, 0.1, 0.5)
                    + A * np.sin(2 * np.pi * frequency_r * t * 1.1) * gauss(t, 0.1, 0.6)
                    + A * np.sin(2 * np.pi * frequency_r * t * 1.2) * gauss(t, 0.1, 0.7)
                )
            )
        elif ultra:
            A = max_sample / 5
            zeros[s][0] = int(
                round(
                    np.sum(A * np.sin(2 * np.pi * nufake * t) * f(nu, t % (0.745 / 40)))
                )
            )  # *np.exp(nufake/1e4)
            zeros[s][1] = zeros[s][0]
        elif ultra2:
            A = max_sample / 25
            zeros[s][0] = int(
                round(
                    (A * np.sum(f(nu, t % 0.745)) - 20000) * np.sin(2 * np.pi * 440 * t)
                )
            )  # *np.exp(nufake/1e4)
            zeros[s][1] = zeros[s][0]

    print(zeros)
    sound = pg.sndarray.make_sound(zeros)

    sound.play()
    pg.time.wait(int(round(1000 * duration)))

finally:
    pg.mixer.quit()

import matplotlib.pyplot as plt

plt.plot(zeros)
plt.show()
