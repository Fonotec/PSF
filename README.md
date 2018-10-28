# PSF
Welcome on the github of PSF (Pulsar Spectral Folder)! PSF is the fastest spectral folder in the local Universe (much faster than those noobs in M31). This readme will explain what the different modules in PSF work. PSF is specifically designed to use pulsar data either live or for after processing. The aim of PSF is to do this as fast as possible, faster than any previous algorithm. Till know several live features exist: live plotting the pulsar signal and live folding of the pulsar signal, the first method is especially usefull for pulsars that have a significant flux like our home pulsar B0329+54, and live folding can be used for pulsars that are fainter like our neighbors pulsar like B2016+28. Furthermore the algorithm will be able in the comming time to save data on the spot when doing simultaneously live folding and live pulsar autoput. In the after processing also determining if weather balloons are present is designed and we are able to determine the period to a very high precission by using a Chi-squared approach. The details of these different features will be discussed in the following sections.

## Requirements
The requirements of our program are written in `requirements.txt`.  Until now the requirements are `numpy`, `scipy`, `matplotlib`, `tkinter`, `astropy`, `numba`, `tqdm`, `ruamel.yaml` and `blimpy`. To get your system up to date with these packages you can use the following pip command:

`pip install -r requirements.txt --user`

## The program
In this section we describe the different module and sub routines in PSF.

To try out the tools, you can run the various examples in the [`examples`](examples/) folder (just run `run.sh` in one of the various folders).

### Main file
The main file of PSF is `main.py`, this file allowes you to run load data of an observation and run an analysis on the data.
For folding and plotting the waterfall plots/pulse profile, you can use `main.py param.yml`, where `param.yml` is the file in which you have indicated what PSF should do. Examples of the syntax of these `.yml` files are in the `examples` folder.

### Observation file
In the observation file `observation.py` constructs a class of Observations that allows you to get the frequency range of the observation and other properties.

### Flagging
In a datafile it is of significant importance that we filter out RFI from the data such that only useful astronomical signals are used, so we do not use the electric cow fence or the encrypted signals from the police on our bands. For this we used a sophisticated flagging routine which we also call 'gras maaien', everything about flagging is in `flagging.py`. Currently the flagging routine is `numba` accelerated, which means it is a faster version due to some pre compilement.

### Data Folding
A pulsar signal is sometimes too weak, to nevertheless observe a pulsar, the data is folded periodically on the period of the pulsar. By doing this the signal over noise of the pulsar is signifantly increased. If we do not fold, this implies that only bright pulsars are visible by eye like PSR B0329+54 and some giant burst from less bright pulsars like the Crab pulsar. In this algorithm the data is folded for each frequency bin seperatly also this part of the program is accelerated by using `numba`. The folding algorithm is present in `folding.py`. On an average machine a folding of 10 minutes of data takes around 3 seconds.

### Waterfall plots 
Using the routines it is possible to produce a folded waterfall plot that shows an intensity map of the frequency and time (0 until period) of the folded data, using this it is possible to determine which frequency bins are important in this data and which bins are dominated by RFI, also it becomes clear using the waterfall plot how the dispersion measure influences the different frequencies by shifting different frequencies differently. The waterfall plot can be found in the `plotTools.py` file which has the function `waterfall` which only needs the argument of the folded 2d array.

### Dispersion Measure correction
For pulsars the dispersion measure is an important parameter which describes the amount of electrons between the pulsar and the observer (the Earth), in the case that electrons are present between the pulsar and the observer different wavelengths are delayed differently according to:
$$ \Delta t = 4.148~\text{ms} DM \cdot \left( \left(\frac{\nu_1}{\text{GHz}}\right)^2 - \left(\frac{\nu_2}{\text{GHz}}\right)^2 \right) $$
In which $DM$ is the dispersion measure in units of $\text{pc}~\text{cm}^{-3}$.

It is also possible to find out the period of a pulsar (by folding the pulse at many periods, and finding out the best period), ask if you want it.
And live pulsar folding is WIP...
An interface, making this all pretty and easy to use is also WIP, a preview is in interface.py.
