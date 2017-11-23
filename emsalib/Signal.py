import matplotlib.pyplot as plt
from .TimeSample import TimeSample
import numpy as np
from scipy import interpolate
import copy

class Signal:
    y = []

    def __init__(self, y):
        self.y = copy.deepcopy(y)
        self.alignX0()

    def updateys(self, ysUpdate):
        self.y = [TimeSample(t, y) for t, y in zip(self.ts(), ysUpdate)]

    def updatets(self, tsUpdate):
        for yi, ti in zip(self.y, tsUpdate):
            yi.t = ti

    def alignX0(self):
        self.updatets(self.ts() - min(self.ts()))

    def plot(self, tstart=0, tend=None, tshift=0):
        plt.plot([yi.t + tshift for yi in self.y[tstart:tend]], [yi.y for yi in self.y[tstart:tend]])
        for yi in self.y[tstart:tend]:
            if yi.peak:
                plt.plot(yi.t + tshift, yi.y, 'ro', ms=3)
            if yi.valley:
                plt.plot(yi.t + tshift, yi.y, 'go', ms=3)

    def mapSynthT(self, synthT):
        self.alignX0()
        tscale = (max(synthT)-min(synthT))/max(self.ts())
        scaledTorig = self.ts()*tscale + min(synthT)
        y_interpolant = interpolate.interp1d(scaledTorig, self.ys(), bounds_error=False, fill_value="extrapolate")
        y_new = y_interpolant(synthT)
        self.y = [TimeSample(t, y) for t, y in zip(synthT, y_new)]

    def concat(self, motif):
        self.y = self.y +  motif.y

    def findIdx(self, ycandidate):
        return self.y.index(ycandidate)

    def subseq(self, start=0, stop=None):
        return Signal(self.y[start:stop])

    def mean(self):
        return np.mean([yi.y for yi in self.y])

    def var(self):
        return np.var([yi.y for yi in self.y])

    def zeroMean(self):
        mean = np.mean(self.ys())
        for yi in self.y:
            yi.y = yi.y - mean

    def ys(self):
        return np.array([yi.y for yi in self.y])

    def ts(self):
        return np.array([yi.t for yi in self.y])

    def resample(self):
        fs = 33
        ps = 1 / fs
        n = np.int16(8192)
        freq = np.linspace(0, fs / 2, num=int(n // 2))
        ts_new = np.arange(min(self.ts()), max(self.ts()), ps)
        ys_interpolant = interpolate.interp1d(self.ts(), self.ys())
        ys_new = ys_interpolant(ts_new)
        self.y = [TimeSample(t, y) for t, y in zip(ts_new, ys_new)]