#!/usr/bin/env python
import numpy as np

def flagData(data):
    noflag = data[:,0]>0
    return noflag
