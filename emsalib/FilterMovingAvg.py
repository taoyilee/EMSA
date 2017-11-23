from . import TimeSeries
import numpy as np
from scipy import signal, interpolate, fftpack


class FilterMovingAvg:
    filterLen = 5

    def __init__(self, filterLen=5):
        self.filterLen = filterLen

    def filter(self, ts):
        win = np.ones(self.filterLen)
        ts.updateys(np.array(signal.convolve(ts.ys(), win, mode='same') / self.filterLen))
