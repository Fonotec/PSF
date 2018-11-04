#!/bin/bash

# Download the observation data if it is not present
if [ ! -e B2217_10-04-2018-withP.fits.gz ]
then 
	echo "Dowloading the observation data"
	./getData.sh
fi

# Run PSF
echo "Run PSF"
if command -v python3 &>/dev/null; then
    python3 ../../main.py B2217+47Param.yml
else 
    python ../../main.py B2217+47Param.yml
fi

