#!/bin/bash

# Download the observation data if it is not present
if [ ! -e B0329+54.2016.11.18.1038.5min.dat ]
then 
	echo "Dowloading the observation data"
	./getData.sh
fi

# Run PSF
echo "Run PSF"
if command -v python3 &>/dev/null; then
    python3 ../../main.py huispulsarParam.yml
else
    python ../../main.py huispulsarParam.yml
fi

