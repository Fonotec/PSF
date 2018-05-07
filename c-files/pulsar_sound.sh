#!/bin/bash
# Rate should be 2136.2304
#pulseaudio -k


export AUDIODRIVER=alsa
export AUDIODEV=hw:1

rm /tmp/sound >/dev/null
mkfifo /tmp/sound
chmod a+rwx /tmp/sound

amixer set "Master" unmute

pasuspender -- play -r 2133 --buffer 512 -c 1 -b 16 -e signed-integer -v 5 -t raw /tmp/sound & 
/home/paulb/sources/pulsar-live 540 4>/tmp/sound |gnuplot -noraise


