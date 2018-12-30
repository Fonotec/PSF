#!/usr/bin/env python
from copy import deepcopy
import numpy as np
from pathlib import Path
from ruamel.yaml import YAML

# https://stackoverflow.com/questions/36831998/how-to-fill-default-parameters-in-yaml-file-using-python
def setdefault_recursively(tgt, default):
    for k in default:
        if isinstance(default[k], dict): # if the current item is a dict,
            # expand it recursively
            setdefault_recursively(tgt.setdefault(k, {}), default[k])
        elif isinstance(tgt, dict):
            # ... otherwise simply set a default value if it's not set before
            tgt.setdefault(k, default[k])

# https://stackoverflow.com/a/38034502
class AttrDict(dict):                            
     """ Dictionary subclass whose entries can be accessed by attributes
         (as well as normally).
     """
     def __init__(self, *args, **kwargs):
         super(AttrDict, self).__init__(*args, **kwargs)
         self.__dict__ = self
 
     @staticmethod
     def from_nested_dict(data):
         """ Construct nested AttrDicts from nested dictionaries. """
         if not isinstance(data, dict):
             return data
         else:
             return AttrDict({key: AttrDict.from_nested_dict(data[key])
                                 for key in data})

class Config(AttrDict):
    """
    # Initialize as:
    param = yamlclass('param.yml')

    # Calling parameters as:
    print(param.FileName)
    print(param.ChiFit.Ntries)

    # These values have been replaced with defaults if the user did not input them
    # The actual user input is still available from param.usercfg.
    """
    def __init__(self,paramyml, defaults=Path(__file__).parent/'defaults.yml'):
        yaml=YAML(typ='safe')

        with open(paramyml,'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        with open(defaults,'r') as ymlfile:
            defaults = yaml.load(ymlfile)

        usercfg = deepcopy(cfg)
        setdefault_recursively(cfg, default=defaults)


        # Input validation can happen here
        assert 'FileName' in usercfg, 'Provide observation parameters'
        assert 'Output' in usercfg, 'Provide output information'
        super(Config, self).__init__(AttrDict.from_nested_dict(cfg)) # Magic...

        self.usercfg = AttrDict.from_nested_dict(usercfg)
        self.defaults= AttrDict.from_nested_dict(defaults)
