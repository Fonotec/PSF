#!/usr/bin/env python
import numpy as np

# class for pulsars

class Pulsar:
    # constructor of the pulsar
    def __init__(self,pulsardata):
        # read the array
        self.ID = pulsardata[0]
        self.name = pulsardata[1]
        self.RAJD = pulsardata[2]
        self.DECJD = pulsardata[3]
        self.period = pulsardata[4]
        self.periodder = pulsardata[5]
        self.DM = pulsardata[6]
        self.RM = pulsardata[7]
        self.W50 = pulsardata[8]
        self.W10 = pulsardata[9]
        self.S400 = pulsardata[10]
        self.S1400 = pulsardata[11]
        self.distance = pulsardata[12]

    # basically get functions of the class
    @property
    def getID(self):
        return self.ID

    @property
    def getName(self):
        return self.name

    @property
    def getCoordinates(self):
        return self.RAJD, self.DECJD

    @property
    def getPeriod(self):
        return self.period

    @property
    def getPeriodDer(self):
        return self.periodder
    
    @property
    def getDM(self):
        return self.DM

    @property
    def getRM(self):
        return self.RM

    @property
    def getW50(self):
        return self.W50

    @property
    def getW10(self):
        return self.W10

    @property    
    def getS400(self):
        return self.S400

    @property    
    def getS1400(self):
        return self.S1400

    @property    
    def getPeriodDM(self):
        return self.period, self.DM

    @property
    def getDistance(self):
        return self.distance

    # calculation functions
    @property
    def getPulseFlux(self):
        return self.S400/self.W50


