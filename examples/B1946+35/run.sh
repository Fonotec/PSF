#!/bin/bash

# Download the observation data if it is not present
if [ ! -e B1946+35_10-04-2018-withP.fits.gz ]
then 
	echo "Dowloading the observation data"
	./getData.sh
fi

# Run PSF
echo "Run PSF"
if command -v python3 &>/dev/null; then
    python3 ../../main.py B1946+35Param.yml 
else 
    python ../../main.py B1946+35Param.yml 
fi

