import numpy as np
from astropy.io import fits
from astropy.time import Time
from pulsarsObjects import Pulsar, load_pulsar_data
from astropy import units as u
from barcen import barcen_times


class Observation:
    def __init__(self, fitsfile):
        hdulist = fits.open(fitsfile)
        header = hdulist[1].header
        self.data = hdulist[1].data
        self.psr_name = header['SRC_NAME']
        self.obs_start_isot = header['DATE-OBS']
        self.mix_freq = header['FREQMIX']

        self.obs_start = Time(self.obs_start_isot, format='isot')
        dt = 64*512/(70e6)
        self.obs_dur = len(self.data) * dt
        self.obs_end = Time(self.obs_start) +  self.obs_dur * u.s
        self.obs_times = np.arange(len(self.data)) * dt

        psrdata = load_pulsar_data(self.psr_name)
        self.pulsar = Pulsar(psrdata, tobs=self.obs_start)

        self.times = barcen_times(self.pulsar, len(self.data), obsstart=self.obs_start)

        self.calc_freqs()

    def calc_freqs(self):
        timevoltage = 1/(70e6) # (s), the time of each voltage measurement
        timefft = 512*timevoltage # (s), the time of each fft block: of each 512 voltage measurements an fft is taken
        dt = timefft * 64 # (s), to reduce the data rate, the sum of 64 ffts is taken
        freqstep = (1/timefft)/1e6 # (MHz), the bandwidth of each frequency bin

        maxfreq = (self.mix_freq+21.4) # (MHz)
        minfreq = maxfreq-35 # (MHz)

        freqs_edges = np.linspace(minfreq, maxfreq, 257) # Frequency bin edges
        freqs = (freqs_edges[1:]+freqs_edges[:-1])/2 # Frequency bin centers
        assert np.allclose(np.diff(freqs_edges), freqstep)
        # The highest frequency is thrown away, to make place for the counter :(
        # Not entirely sure if it was indeed the highest one, we still need to check that
        self.freq_edges = freqs_edges[:-1]
        self.freq = freqs[:-1]

