#!/bin/bash

# Download the observation data if it is not present
if [ ! -e B0531+21_10-04-2018.dat ]
then 
	echo "Dowloading the observation data"
	./getData.sh
fi

# Run PSF
echo "Run PSF"
if command -v python3 &>/dev/null; then
    python3 ../../main.py crabpulsarParam.yml
else
    python ../../main.py crabpulsarParam.yml
fi

