#!/usr/bin/env python
import numpy as np
from astropy.time import Time
from astropy import units as u

# Loading the data
def load_pulsar_data(pulsar_name, pulsarcat_file='pulsarcat.csv'):
    # read the data of the pulsar database
    pulsardata = np.genfromtxt(pulsarcat_file, delimiter=",", dtype=None, encoding='utf-8', names=True, missing_values="*")
    # Find the index of the correct pulsar
    matches = np.where((pulsardata['NAME'] == pulsar_name) | (pulsardata['PSRJ'] == pulsar_name))

    # check if we actually found the pulsar in the data base
    if (len(matches) == 0):
        print('Your defined pulsar was not found in the database')
        print('Program exits with an ERROR!!')
        exit(1)

    pulsardata_row = pulsardata[matches[0]]
    return pulsardata_row

# class for pulsars
class Pulsar:
    # constructor of the pulsar
    def __init__(self, pulsardata, tobs=Time.now()):
        # read the array, and make every object accessible like pulsar.period
        for i in pulsardata.dtype.names:
            setattr(self, i, pulsardata[i][0])

        self.distance = pulsardata['DIST']
        self.period = self.currentPeriod(Time.now())

    
    # The period that the pulsar has now, considering the first period derivative
    def currentPeriod(self, tobs=Time.now()):
        timediff = (tobs - Time(self.PEPOCH, format='mjd')).to(u.s).value
        return self.P0 + self.P1 * timediff

    @property
    def getPeriod(self):
        return self.period

    # calculation functions
    @property
    def getPulseFlux(self):
        return self.S400/self.W50
