import matplotlib
from .TimeSeries import TimeSeries
from .TimeSample import TimeSample

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
        self.labelPeakValley(ts)

    def labelPeakValley(self, ts : TimeSeries, **kwargs):
        search_order = kwargs.get('search_order', 5)
        peaks_idx = np.array(signal.argrelmax(ts.ys, order=search_order))[0]
        ts.setPeak(peaks_idx)
        valleys_idx = np.array(signal.argrelmin(ts.ys, order=search_order))[0]
        ts.setValley(valleys_idx)