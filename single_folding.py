import numpy as np
from numba import jit, guvectorize, float32, int32, float64, int64, boolean


@jit(nopython=True)
def fold_per_fbin(intensity, time_array, period, nbins, flagged):
    time_num_points = intensity.size
    # This is mapped to a phase in the period
    phases = time_array % period

    # This function folds everything in some number of phasebins, so that
    # everything is linearly rebinned in these bins.
    deltat_phasebin = period / nbins
    # The center of phasebin n is dtpb*(n+1/2)
    phasebins = np.arange(time_num_points) * period / nbins + deltat_phasebin
    # So that means that some phase p, corresponds to bin n=p/dtpb-1/2
    phasebin_n = phases / deltat_phasebin - 1 / 2
    lower_inds = np.floor(phasebin_n).astype(np.int64) % nbins
    upper_inds = (lower_inds + 1) % nbins

    upper_norm = (
        phasebin_n % 1
    )  # The modulo 1 takes care of the edge case if n is negative.
    lower_norm = 1 - upper_norm

    # An example of what this does: suppose Period=0.4 s, and phasebins = [0.05,0.15,0.25,0.35],
    # then the phase 0.09 would get a phasebin_n of 0.09/0.1-0.5=0.4.
    # That would give a lower_ind = 0, higher_ind=1, with lower_norm=0.6, higher_norm=0.4
    # Which is what we want.
    # For phase = 0.04, phasebin_n=-0.1, so the lower_ind = -1 % 4 = 3, and the higher_ind = 0.
    # upper_norm = -0.1 % 1 = 0.9, and lower_norm = 0.1.

    upper_norm[flagged] = 0
    lower_norm[flagged] = 0

    foldedarray = np.zeros(nbins)  # This is where the folded curve will live
    # Because we would like the average of each phasebin, a weights array is created
    normarray = np.zeros(nbins)

    # Looping over the time indices in combination with numba.jit turned out to be faster than np.add.at
    for i in range(time_num_points):
        foldedarray[lower_inds[i]] += lower_norm[i] * intensity[i]
        foldedarray[upper_inds[i]] += upper_norm[i] * intensity[i]
        normarray[lower_inds[i]] += lower_norm[i]
        normarray[upper_inds[i]] += upper_norm[i]

    proto_normed_folded = foldedarray / normarray
    normed_folded = proto_normed_folded / proto_normed_folded.sum()
    return normed_folded
