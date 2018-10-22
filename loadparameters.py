#!/usr/bin/env python
import numpy as np
from ruamel.yaml import YAML

class yamlclass:
    def __init__(self,paramyml):
        
        yaml=YAML(typ='safe')

        with open('test.yml','r') as ymlfile:
            cfg = yaml.load(ymlfile)


        # Read the Observation parameters from the YAML file
        try:
            obsdict = cfg['Observation']
        except:
            YAMLerr('Observation not given.')
            exit(-1)

        self.Filename = obsdict['Filename']
        self.RawData = int(obsdict['RawData'])
        if self.RawData==0:
            self.ObsDate = obsdict['ObsDate']
            self.ObsTime = obsdict['ObsTime']
            self.PulsarName = obsdict['PulsarName']
            self.CentreFreq = obsdict['CentreFreq']

        # Read the folding parameters from the YAML file
        try:
            folding = cfg['Folding']
        except:
            YAMLerr('Folding not given.')
            exit(-1)

        self.nbins = folding['nbins']
        self.nbinsdedisp = folding['nbinsdedisp']

        # Read the Output parameters from the YAML file
        try:
            output = cfg['Output']
        except:
            YAMLerr('Output not specified.')
            exit(-1)

        self.OutputDir = output['OutputDit']
        self.ConvertRaw = output['ConvertRaw']




        dochi = True
        try:
            chifit = cfg['ChiFit']
        except:
            dochi = False



        domaaien = True
        try:
            Grasmaaien = cfg['GrasMaaier']
        except:
            domaaien = False

    def YAMLerr(self,string):
        print('YAML ERROR: '+string)








