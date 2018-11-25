#!/usr/bin/env python
import numpy as np


def startScreen(version):
    # total display length
    totallen = 70
    # make a hashtag line with this length
    hashline = "#" * totallen
    # name of the code
    name = "PSF (PULSAR SPECTRAL FOLDER)"
    # make an array of the version
    version = "VERSION " + version
    # length of hashtags on the left and right
    minlen = 3
    # make the minimum hashtag string
    hashmin = "#" * minlen
    authors = "AUTHORS:"

    # print the hashtag line
    hashLine()
    printString(name)
    hashLine()
    printString(version)
    hashLine()
    printString(authors)
    printString("REINIER KOET, ROI KUGUL,")
    printString("FOLKERT NOBELS, ROLAND TIMMERMAN")
    printString("AND EWOUD WEMPE")
    hashLine()
    printString("THE AUTHORS THANK YOU FOR USING PSF, THE FASTEST PULSAR")
    printString("SPECTRAL FOLDING CODE IN THE LOCAL UNIVERSE")
    hashLine()


def printString(string, lengthside=3, totallength=70):
    lenstr = len(string)
    spacing = (totallength - 2 * lengthside - lenstr) / 2
    floorspacing = int(np.floor(spacing))
    if spacing % 1 == 0:
        print(
            "#" * lengthside
            + " " * floorspacing
            + string
            + " " * floorspacing
            + "#" * lengthside
        )
    else:
        print(
            "#" * lengthside
            + " " * floorspacing
            + string
            + " " * (floorspacing + 1)
            + "#" * lengthside
        )


def hashLine(characters=70):
    print("#" * characters)
