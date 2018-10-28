#!/usr/bin/env python

from collections import defaultdict
   
# https://stackoverflow.com/questions/28385822/reading-data-separated-by-colon-per-line-in-python
def filterBankReadMetaData(filename):
    result = defaultdict(list)
    with open(filename) as inf:
        print(inf)
        for line in inf:
            name, score = line.split(": ", 1)
            name = name.rstrip()
            score = score.rstrip('\n')
            result[name].append(score)
    return result






