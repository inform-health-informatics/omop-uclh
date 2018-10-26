"""Module hosting classes that return fake data

[description]
"""
import pandas as pd
import numpy as np
import datetime as dt


class TwoD():
    # generic methods such as creating time series etc

    def __init__(self, spell, cadence=None):

        self.spell = spell

    def gen_time_series(self, cadence=None):
        # return times by natural cadence
        # - daily bloods
        # - regular ward obs
        # - close monitoring in critical care
        # - [ ] @TODO: (2018-10-26) implement missingness
        # - [ ] @TODO: (2018-10-26) implemnent jitter so times don't line up

        # default cadence
        if cadence is None:
            cadence = '1D'

        ts = pd.date_range(self.spell.start, self.spell.stop, freq=cadence)

        return ts



class Lactate(TwoD):

    # - [ ] @TODO: (2018-10-26) implement ABC; require concept mapping

    # calls parent's init by default so you get time series for free
    def simulate(self, cadence=None):
        ts = self.gen_time_series(cadence)
        vals =  [np.random.lognormal() for i in ts]
        return pd.DataFrame.from_dict({'timestamp': ts, 'lacate': vals})

