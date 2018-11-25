#!/usr/bin/env python
import numpy as np
from numba import njit
import numba as nb


@njit
def moving_average(a, n=3):
    assert n % 2 == 1
    # b = np.pad(a, (n//2,n//2), 'symmetric')
    b = np.concatenate((a[n // 2 - 1 :: -1], a, a[: -n // 2 : -1]))
    ret = np.cumsum(b)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1 :] / n


@njit
def pyramid_average(a, n=5):
    return moving_average(moving_average(a, n // 2 + 1), n // 2 + 1)


def flagData(data, nwindow=100001, signific=5, filtertype=0, badneighbors=4):
    return np.copy(
        flagDataV(np.copy(data.T), nwindow, signific, filtertype, badneighbors).T
    )


@nb.guvectorize(
    [(nb.float64[:], nb.int64, nb.int64, nb.int64, nb.int64, nb.boolean[:])],
    "(n),(),(),(),()->(n)",
    target="parallel",
)
def flagDataV(dset, nwindow, signific, filtertype, badneighbors, res):
    # Filtertype: 0 for pyramid, 1 for tophat
    indbad = dset == 0

    # Smoothing is done in log-space
    # That removes the effect of outliers on the smoothed function.
    if filtertype == 1:
        smoothed = np.exp(moving_average(np.log(dset), n=nwindow))
    else:
        smoothed = np.exp(pyramid_average(np.log(dset), n=nwindow))
    residuals = dset - smoothed

    percs = np.percentile(residuals, [25, 75])
    std = (percs[1] - percs[0]) / 1.349  # Use a more robust std estimator

    indbad |= residuals > signific * std
    indbad |= residuals < -signific * std
    # For each bad point, also flag its nearest neighbors
    for _ in range(badneighbors):
        indbad[1:] = indbad[1:] | indbad[:-1]
        indbad[:-1] = indbad[1:] | indbad[:-1]
    res[:] = indbad
