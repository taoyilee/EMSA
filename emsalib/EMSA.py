import matplotlib
from . import TimeSeries
from .FilterToolbox import FilterToolbox
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, interpolate, fftpack


class EMSA:
    flt = None

    def __init__(self, flt_type='ma', **kwargs):
        self.filterLen = kwargs.get('filterLen', 5)
        self.flt = FilterToolbox(type=flt_type,filterLen=self.filterLen)

    def process(self, ts : TimeSeries ):
        ts.resample()
        ts.zeroMean()
        self.flt.filter(ts)
