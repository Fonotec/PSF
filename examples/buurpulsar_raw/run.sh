#!/bin/bash

# Download the observation data if it is not present
if [ ! -e B2016+28_406MHz_2017-12-30.raw ]
then 
	echo "Dowloading the observation data"
	./getData.sh
fi

# Run PSF
echo "Run PSF"
if command -v python3 &>/dev/null; then
    python3 ../../main.py buurpulsarRawParam.yml
else 
    python ../../main.py buurpulsarRawParam.yml
fi

