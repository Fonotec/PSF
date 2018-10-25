#!/usr/bin/env python
import numpy as np
from ruamel.yaml import YAML
from copy import deepcopy

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
     def __init__(self, *args, dict_data=None, **kwargs):
         if dict_data is None:
             super(AttrDict, self).__init__(*args, **kwargs)
             self.__dict__ = self
         else:
             super(AttrDict, self).__init__(self.from_nested_dict(dict_data))
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
    def __init__(self,paramyml, defaults='defaults.yml'):
        yaml=YAML(typ='safe')

        with open(paramyml,'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        with open('defaults.yml','r') as ymlfile:
            defaults = yaml.load(ymlfile)

        usercfg = deepcopy(cfg)
        setdefault_recursively(cfg, default=defaults)


        # Input validation can happen here
        assert 'FileName' in usercfg, 'Provide observation parameters'
        assert 'Output' in usercfg, 'Provide output information'
        super(Config, self).__init__(dict_data=cfg) # Magic...

        self.usercfg = AttrDict(usercfg)
        self.defaults= AttrDict(defaults)
