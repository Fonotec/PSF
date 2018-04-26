#!/usr/bin/env python
# coding: utf-8

import argparse
from astropy.io import fits
from loadData import loader

parser = argparse.ArgumentParser(description='')
parser.add_argument('-d', '--datafile', required=True, help='The location of the *.raw or *.dat data file.')
parser.add_argument('-f', '--fitsfile', required=True, help='The location of the resulting *.fits fits file.')
parser.add_argument('--pulsarname', required=True, help='The name of the pulsar, as noted in the database, \'pulsardata.txt\'.')
parser.add_argument('--frequencymix', type=float, required=True, help='The mixing frequency set on the receiver in MHz (e.g. 420)')
parser.add_argument('--obstime', required=True, help='The start datetime of the observation, in isot format (e.g. 2018-03-10T14:00:00)')
args = parser.parse_args()

data = loader(args.datafile)
header = fits.Header()
header['SRC_NAME'] = args.pulsarname
header['FREQMIX'] = args.frequencymix
header['DATE-OBS'] = args.obstime
hdu = fits.ImageHDU(data, header)
hdu.writeto(args.fitsfile)
