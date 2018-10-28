#!/bin/bash

# Download the observation data if it is not present
if [ ! -e B0329+54_10-04-2018.fits.gz ]
then 
	echo "Dowloading the observation data"
	./getData.sh
fi

# Run PSF
echo "Run PSF"
python3 ../../main.py huispulsarParam.yml

