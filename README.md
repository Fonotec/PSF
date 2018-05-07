# PSF
Welcome on the github of PSF (Pulsar Spectral Folder)! PSF is the fastest spectral folder in the local Universe (much faster than those noobs in M31). This readme will explain what the different modules in PSF work. PSF is specifically designed to use pulsar data either live or for after processing. The aim of PSF is to do this as fast as possible, faster than any previous algorithm. Till know several live features exist: live plotting the pulsar signal and live folding of the pulsar signal, the first method is especially usefull for pulsars that have a significant flux like our home pulsar B0329+54, and live folding can be used for pulsars that are fainter like our neighbors pulsar like B2016+28. Furthermore the algorithm will be able in the comming time to save data on the spot when doing simultaneously live folding and live pulsar autoput. In the after processing also determining if weather balloons are present is designed and we are able to determine the period to a very high precission by using a Chi-squared approach. The details of these different features will be discussed in the following sections.

## Requirements
The requirements of our program are written in `requirements.txt`.  Until now the only requirements are `numpy`, `scipy`, `matplotlib`, `tkinter`, `astropy` and `tqdm`. To get your system up to date with these packages you can use the following pip command:

`pip install -r requirements.txt --user`

## The program
In this section we describe the different module and sub routines in PSF.

### Main file
The main file of PSF is `main.py`, this file allowes you to run load data of an observation and run an analysis on the data.

### Start screen
PSF has an start screen which describes the motto of PSF and shown the authors of PSF. The start screen has its own module and this module can be found in `startscreen.py`. 

### observation file
In the observation file `observation.py` constructs a class of Observations that allowes you to get the frequency range of the observation and other properties.
