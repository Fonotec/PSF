#!/usr/bin/env python
import numpy as np
from ruamel.yaml import YAML

class yamlclass:
    def __init__(self,paramyml):
        
        yaml=YAML(typ='safe')

        with open(paramyml,'r') as ymlfile:
            cfg = yaml.load(ymlfile)


        # Read the Observation parameters from the YAML file
        try:
            obsdict = cfg['Observation']
        except:
            YAMLerr('Observation not given.')
            exit(-1)

        # Store the variables of the part in variables in the class
        self.FileName = obsdict['FileName']
        self.RawData = int(obsdict['RawData'])
        if self.RawData==0:
            self.ObsDate = obsdict['ObsDate']
            self.ObsTime = obsdict['ObsTime']
            self.PulsarName = obsdict['PulsarName']
            self.CentreFreq = float(obsdict['CentreFreq'])

        # Read the folding parameters from the YAML file
        try:
            folding = cfg['Folding']
        except:
            YAMLerr('Folding not given.')
            exit(-1)

        # Store the folding parameters in the class
        self.nbins = int(folding['nbins'])
        self.nbinsdedisp = int(folding['nbinsdedisp'])

        # Read the Output parameters from the YAML file
        try:
            output = cfg['Output']
        except:
            YAMLerr('Output not specified.')
            exit(-1)

        # Store the output specific parameters in the class
        self.OutputDir = output['OutputDir']
        self.ConvertRaw = int(output['ConvertRaw'])

        # Check if we do the Chi Fit
        self.dochi = True
        try:
            chifit = cfg['ChiFit']
        except:
            self.dochi = False

        # Store the Chi Fit parameters if we do the Chi Fit.
        if self.dochi:
            self.Plow = float(chifit['Plow'])
            self.Phigh = float(chifit['Phigh'])
            self.Ntries = int(chifit['Ntries'])
            self.fitfunc = chifit['FitFunc']

        # Check if we do grasmaaien 
        self.domaaien = True
        try:
            Grasmaaien = cfg['GrasMaaier']
        except:
            self.domaaien = False

        # Store the maaien parameters if we are `aan het grasmaaien'
        if self.domaaien:
            self.STDCut = float(Grasmaaien['STDCut'])
            self.Meantype = Grasmaaien['Meantype']

    def YAMLerr(self,string):
        print('YAML ERROR: '+string)

    
# Initialize as:
# param = yamlclass('param.yml')
# Calling parameters as:
# print(param.FileName)
# print(param.STDCut)





