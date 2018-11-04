import numpy as np
from astropy.io import fits
from astropy.time import Time
from pulsarsObjects import Pulsar, load_pulsar_data
from astropy import units as u
from barcen import barcen_times, barcen_freqs
from loadData import loader
from pathlib import Path
from filterBank import filterBankReadMetaData
from blimpy import Waterfall

def calc_central_freqs(mix_freq, throwhighestfreqaway=True):
    timevoltage = 1/(70e6) # (s), the time of each voltage measurement
    timefft = 512*timevoltage # (s), the time of each fft block: of each 512 voltage measurements an fft is taken
    dt = timefft * 64 # (s), to reduce the data rate, the sum of 64 ffts is taken
    freqstep = (1/timefft)/1e6 # (MHz), the bandwidth of each frequency bin

    maxfreq = (mix_freq+21.4) # (MHz)
    minfreq = maxfreq-35 # (MHz)

    freqs_edges = np.linspace(minfreq, maxfreq, 257) # Frequency bin edges
    freqs = (freqs_edges[1:]+freqs_edges[:-1])/2 # Frequency bin centers
    assert np.allclose(np.diff(freqs_edges), freqstep)
    # Previously wrong! 
    # The lowest frequency is instead thrown away to make place for the packet counter. 
    # Source: c-files/pulsar-live2.c, where bin 256 = lowest frequency is replaced.
    if throwhighestfreqaway:
        return freqs[1:]
    else:
        return freqs

class Observation:
    def __init__(self, cfg=None, fitsfile=None):
        if fitsfile is None:
            fileformat = cfg.FileFormat if 'FileFormat' in cfg else cfg.FileName
            filename = cfg.FileName
        else:
            fileformat="fits"
            filename = fitsfile

        if fileformat.endswith('fits') or fileformat.endswith('fits.gz'):
            self.using_fits = True
            hdulist = fits.open(filename)
            header = hdulist[1].header
            self.data = hdulist[1].data
            self.psr_name = header['SRC_NAME']
            self.obs_start_isot = header['DATE-OBS']
            self.mix_freq = header['FREQMIX']
        elif fileformat.endswith('fil'):
            self.using_fits = False 
            obs = Waterfall(filename)
            header = obs.header
            self.psr_name = header[b'source_name'].decode('utf-8')[4:]
            self.obs_start_isot = header[b'tstart']
            # Tammo-Jan doesn't store the mix frequency
            self.mix_freq = header[b'fch1']-21.668359375
            self.data = obs.data[:,:,:255]
            #raise NotImplementedError('Filterbank supported yet!')
        else:
            self.using_fits = False
            self.psr_name = cfg.ObsMetaData.PulsarName
            self.obs_start_isot = cfg.ObsMetaData.ObsDate
            self.mix_freq = cfg.ObsMetaData.MixFreq
            if fileformat.endswith('fil'):
                raise NotImplementedError('Filterbank supported yet!')
            elif fileformat.endswith('raw'):
                assert cfg.RawData, 'Need to supply the metadata!'
                self.data = loader(cfg.FileName).astype(np.uint32)
            else:
                raise ValueError('Unrecognized format')

        print(self.psr_name)
        print(self.obs_start_isot)
        print(self.data)

        if fileformat.endswith('fil'):
            self.obs_start = Time(self.obs_start_isot,format='jd')
        else:
            self.obs_start = Time(self.obs_start_isot)
        dt = 64*512/(70e6)
        self.obs_dur = len(self.data) * dt
        self.obs_end = self.obs_start +  self.obs_dur * u.s
        self.obs_times = np.arange(len(self.data)) * dt
        self.obs_middle = self.obs_dur*u.s/2 + self.obs_start

        if self.using_fits and len(hdulist)>2:
            self.chisqperiod = hdulist[2].header['bestp']
        else:
            self.chisqperiod = None

        self.pulsar = Pulsar(pulsarname=self.psr_name, tobs=self.obs_start, chisqperiod=self.chisqperiod)

        self.times = barcen_times(self.pulsar, len(self.data), obsstart=self.obs_start)
        self.freq_uncor = calc_central_freqs(self.mix_freq)
        self.freq = barcen_freqs(self.pulsar, self.freq_uncor, self.obs_middle) # Probably unnecessary...
