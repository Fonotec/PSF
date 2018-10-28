#!/bin/bash

# Download the observation data if it is not present
if [ ! -e B2016+28_10-04-2018.fits.gz ]
then 
	echo "Dowloading the observation data"
	./getData.sh
fi

# Run PSF
echo "Run PSF"
if command -v python3 &>/dev/null; then
    python3 ../../main.py buurpulsarParam.yml
else 
    python ../../main.py buurpulsarParam.yml
fi

