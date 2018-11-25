#!/usr/bin/env python
import numpy as np
from folding import timeFolding
from single_folding import fold_per_fbin


def dedispersion(folded, obs, period, DM, freq_fold_bins=500):
    time_fold_bins = len(folded)
    folded_times = np.arange(time_fold_bins) * period / time_fold_bins
    dedispersed_times = folded_times[:, np.newaxis] - 4.148e3 * DM * obs.freq ** (-2)
    folded_dedispersed = fold_per_fbin(
        folded.flatten(),
        dedispersed_times.flatten(),
        period,
        freq_fold_bins,
        folded.flatten() == 0,
    )
    return folded_dedispersed
