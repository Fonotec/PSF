import numpy as np
from astropy.io import fits
from astropy.time import Time
from pulsarsObjects import Pulsar, load_pulsar_data
from astropy import units as u
from barcen import barcen_times, barcen_freqs
from loadData import loader
from pathlib import Path
from blimpy import Waterfall
from paramObj import Config


def calc_central_freqs(mix_freq, throwhighestfreqaway=True):
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
    assert np.allclose(np.diff(freqs_edges), freqstep)
    # Previously wrong!
    # The lowest frequency is instead thrown away to make place for the packet counter.
    # Source: c-files/pulsar-live2.c, where bin 256 = lowest frequency is replaced.
    if throwhighestfreqaway:
        return freqs[1:]
    else:
        return freqs


class Observation:
    def __init__(self, fn_or_cfg):
        if type(fn_or_cfg) == Config:
            cfg = fn_or_cfg
            filename = cfg.FileName
            fileformat = (
                cfg.FileFormat
                if "FileFormat" in cfg
                else cfg.FileName.rstrip(".gz").split(".")[-1]
            )
        elif type(fn_or_cfg) == str:
            cfg = None
            filename = fn_or_cfg
            fileformat = filename.rstrip(".gz").split(".")[-1]
        self.fileformat = fileformat

        self.chisqperiod = None
        if fileformat == "fits":
            hdulist = fits.open(filename)
            header = hdulist[1].header
            self.data = hdulist[1].data
            self.psr_name = header["SRC_NAME"]
            self.obs_start_isot = header["DATE-OBS"]
            self.obs_start = Time(self.obs_start_isot)
            self.mix_freq = header["FREQMIX"]
            if len(hdulist) > 2:
                self.chisqperiod = hdulist[2].header["bestp"]
        elif fileformat == "fil":
            obs = Waterfall(filename)
            header = obs.header
            self.psr_name = header[b"source_name"].decode("utf-8")[4:]
            self.obs_start_isot = header[b"tstart"]
            self.obs_start = Time(self.obs_start_isot, format="mjd")
            # Tammo-Jan doesn't store the mix frequency
            self.mix_freq = header[b"fch1"] - 21.668359375
            # These files have the frequency axis in decending, and include an extra unnecessary axis.
            self.data = np.squeeze(obs.data[:, :, -2::-1]).astype(np.uint16)
            # Some files have a missing frequency list for some reason. To avoid errors after folding, add some artificial data...
            self.data[:, ~np.any(self.data, axis=0)] += 65535
        else:
            assert (
                cfg.ObsMetaData
            ), "Need to supply the metadata: observation time, mixing frequency and pulsar!"
            self.data = loader(cfg.FileName).astype(np.uint32)

        if cfg is not None and cfg.ObsMetaData:
            # Overwrite with metadata from the Config if present
            self.psr_name = cfg.ObsMetaData.PulsarName
            self.obs_start_isot = cfg.ObsMetaData.ObsDate
            self.obs_start = Time(self.obs_start_isot)
            self.mix_freq = cfg.ObsMetaData.MixFreq

        dt = 64 * 512 / (70e6)
        self.obs_dur = len(self.data) * dt
        self.obs_end = self.obs_start + self.obs_dur * u.s
        self.obs_times = np.arange(len(self.data)) * dt
        self.obs_middle = self.obs_dur * u.s / 2 + self.obs_start

        self.pulsar = Pulsar(
            pulsarname=self.psr_name, tobs=self.obs_start, chisqperiod=self.chisqperiod
        )

        self.times = barcen_times(self.pulsar, len(self.data), obsstart=self.obs_start)
        self.freq_uncor = calc_central_freqs(self.mix_freq)
        self.freq = barcen_freqs(
            self.pulsar, self.freq_uncor, self.obs_middle
        )  # Probably unnecessary...
