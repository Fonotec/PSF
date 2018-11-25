#!/usr/bin/env python
import numpy as np


def loader(name):
    # The data obtained by the Dwingeloo radio
    # radio telescope is rather cumbersome and
    # stored as unsigned ints, because of this
    # it is required that a new data type is
    # defined that is an unsigned 32 bit integer
    # number:
    unsingeddatat = np.dtype(np.uint32)

    # Because the endianness of Dwingloo telescope
    # is different than the endianness on our
    # machines we need to change the byte order:
    unsingeddatat = unsingeddatat.newbyteorder("S")
    # for more information regarding endiannes see
    # https://en.wikipedia.org/wiki/Endianness

    # After constructing the correct data type we can try
    # loading the data by using fromfile.

    try:
        data_array = np.fromfile(name, dtype=unsingeddatat)
    except FileNotFoundError:
        print("This file could not be found.")
        exit(1)

    # Until now the data is just a 1 times many array,
    # which is quite useless for our analysis. We want
    # that the data is stored as time vertical and horizontal
    # the frequency bins.
    # We know that we have 256 seperate colums of which the
    # 0th element is an arbitary counter and the remaining
    # ones are the frequency bins.
    # This means the array needs to be reshaped as follows:

    return np.reshape(data_array, (int(len(data_array) / 256), 256))[:, 1:]
