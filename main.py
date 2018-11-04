#!/usr/bin/env python
# coding: utf-8
# importing all the used modules
import numpy as np
import matplotlib.pyplot as plt
import argparse
from pathlib import Path

from startscreen import startScreen
from folding import timeFolding
from flagging import flagData
from dispersionMeasure import dedispersion
from observation import Observation
from paramObj import Config
from makefitsfile import raw2fits

startScreen('1.1.0')

parser = argparse.ArgumentParser(description='Pulsar folding!')
parser.add_argument('paramfile', help='A parameter file containing all the necessary data. Overwrites any other arguments.')
args = parser.parse_args()

# Create an object containing all useful pulsar properties
print("Loading parameters")
cfg = Config(args.paramfile)
print("Loading data")
obs = Observation(cfg)
pulsar = obs.pulsar
twodarray = obs.data

# read the literature value of the period and the dispersion measure
period = pulsar.period
DM = pulsar.DM

# Time resolution of the telescope
dt = (512*64)/(70e6)

# Array with the bandwith
frequencyarray = obs.freq

# this part should be RFI flagging something like:
# noflag = flagging(twodarray)

if cfg.GrasMaaier:
    print("Flagging bad data")
    flagparams = dict()
    flagparams['signific'] = cfg.GrasMaaier.STDCut
    flagparams['filtertype'] = dict(pyramid=0, tophat=1)[cfg.GrasMaaier.FilterType]
    flagparams['nwindow'] = cfg.GrasMaaier.FilterWindow
    flag = flagData(twodarray, **flagparams)
else:
    flag = (obs.data) == 0 

Path(cfg.Output.OutputDir).mkdir(parents=True, exist_ok=True) 

# calculate the folded array
if cfg.Folding:
    print("Folding")
    foldedarray = timeFolding(twodarray, cfg.Folding.nbins, period, flagged = flag, corrected_times=obs.times)

    print("Done folding")
    # make a waterfall plot of the result
    plt.matshow((foldedarray-foldedarray.mean(axis=0))/foldedarray.std(axis=0))
    if cfg.Output.SavePlots:
        plt.savefig(cfg.Output.OutputDir+"/waterfall.pdf")
    plt.show()
    print("Dedispersing")
    # do the dedispersion
    pulse_profile = dedispersion(foldedarray, obs, period, obs.pulsar.DM, freq_fold_bins=cfg.Folding.nbinsdedisp)

    # plot the final pulse profile
    plt.plot(pulse_profile)
    if cfg.Output.SavePlots:
        plt.savefig(cfg.Output.OutputDir+"/dedisp_pulse.pdf")
    plt.show()

if obs.fileformat != 'fits' and cfg.Output.ConvertRaw:
    raw2fits(obs.data, cfg.Output.OutputDir+"/"+Path(cfg.FileName).stem+".fits", **cfg.ObsMetaData)
