#!/bin/bash

# Download the observation data if it is not present
if [ ! -e 2017-09-20-07%3A05%3A00_B0329+54.fil ]
then 
	echo "Dowloading the observation data"
	./getData.sh
fi

# Run PSF
echo "Run PSF"
if command -v python3 &>/dev/null; then
    python3 ../../main.py huispulsarFilterbankParam.yml
else 
    python ../../main.py huispulsarFilterbankParam.yml
fi

