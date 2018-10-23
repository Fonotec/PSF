#!/bin/bash

# Download the observation data if it is not present
if [ ! -e 2018-01-19-21%3A16%3A50_B1133+16.txt ]
then 
	echo "Dowloading the observation data"
	./getData.sh
fi

# Run PSF
echo "Run PSF"
../../main.py huispulsarFilterbankParam.yml

