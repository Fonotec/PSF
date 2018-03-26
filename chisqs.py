from jug import TaskGenerator, mapreduce
from observation import Observation
from dispersionMeasure import dedispersion
from folding import timeFolding
from flagging import flagData
import numpy as np
from functools import lru_cache

print("loading data")
obs = Observation("./data/obs-10-04-2018/B2016+28_10-04-2018.fits")
print("flagging")
obs.flag = flagData(obs.data)

time_fold_bins = 1000
freq_fold_bins = 100

@TaskGenerator
def chisq(period, DM):
    folded = timeFolding(obs.data, time_fold_bins, period, flagged=obs.flag, corrected_times=obs.times)
    dedispersed = dedispersion(folded, obs, period, DM, freq_fold_bins=freq_fold_bins)
    chisq = ((dedispersed-dedispersed.mean())**2).sum()
    return chisq

@TaskGenerator
def saveresults(params, results):
    periods = np.array(params)[:,0]
    DMS = np.array(params)[:,1]
    np.savez("chisqs.npz", period = periods, DM = DMS, chisq = results)

DMS = [obs.pulsar.DM]
periods = np.linspace(0.5578,0.5581,2000)
args = [(period, DM) for DM in DMS for period in periods]
results = mapreduce.currymap(chisq, args, map_step=10)
saveresults(args, results)
