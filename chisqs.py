from jug import TaskGenerator, mapreduce
from observation import Observation
from dispersionMeasure import dedispersion
from folding import timeFolding
from flagging import flagData
import numpy as np
from functools import lru_cache

obsfilelist = [
    "./data/obs-10-04-2018/B0125+25-04-2018.fits",
    "./data/obs-10-04-2018/B0329+54_10-04-2018.fits",
    "./data/obs-10-04-2018/B1946+35_10-04-2018.fits",
    "./data/obs-10-04-2018/B2111+46_10-04-2018.fits",
    "./data/obs-10-04-2018/B2154+40_10-04-2018.fits",
    "./data/obs-10-04-2018/B2217_10-04-2018.fits",
    "./data/obs-10-04-2018/B2310+42-04-2018.fits",
]
print("loading data")
obs = Observation("./data/obs-10-04-2018/B2310+42-04-2018.fits.gz")
print("flagging")
obs.flag = flagData(obs.data)

time_fold_bins = 1000
freq_fold_bins = 100


@TaskGenerator
def chisq(period, DM):
    folded = timeFolding(
        obs.data, time_fold_bins, period, flagged=obs.flag, corrected_times=obs.times
    )
    dedispersed = dedispersion(folded, obs, period, DM, freq_fold_bins=freq_fold_bins)
    chisq = ((dedispersed - dedispersed.mean()) ** 2).sum()
    return chisq


@TaskGenerator
def saveresults(params, results, filename):
    periods = np.array(params)[:, 0]
    DMS = np.array(params)[:, 1]
    np.savez(filename, period=periods, DM=DMS, chisq=results)


DMS = [obs.pulsar.DM]
width = 3e-4 * obs.pulsar.period  # Maybe this is observation duration dependent?
periods = np.linspace(
    obs.pulsar.period * (1 - width), obs.pulsar.period * (1 + width), 5000
)
args = [(period, DM) for DM in DMS for period in periods]
results = mapreduce.currymap(chisq, args, map_step=10)
saveresults(args, results, f"chisqs.{obs.pulsar.NAME.decode('utf-8')}.npz")
