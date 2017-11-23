import matplotlib.pyplot as plt
from .TimeSample import TimeSample
import numpy as np
from scipy import interpolate

class Signal:
    y = []

    def __init__(self, y):
        self.y = []
        for yi in y:
            self.y.append(TimeSample(yi.t, yi.y))
            if yi.peak:
                self.y[-1].setPeak()
            if yi.valley:
                self.y[-1].setValley()
        self.alignX0()

    def alignX0(self):
        x0 = self.y[0].t
        for yi in self.y:
            yi.t = yi.t - x0

    def plot(self, tstart=0, tend=None, tshift=0):
        plt.plot([yi.t + tshift for yi in self.y[tstart:tend]], [yi.y for yi in self.y[tstart:tend]])
        for yi in self.y[tstart:tend]:
            if yi.peak:
                plt.plot(yi.t + tshift, yi.y, 'ro', ms=3)
            if yi.valley:
                plt.plot(yi.t + tshift, yi.y, 'go', ms=3)

    def mapSynthT(self, synthT):
        tscale = (max(synthT)-min(synthT))/(max(self.ts())-min(self.ts()))
        scaledTorig = (self.ts() - min(self.ts()))*tscale + min(synthT)
        y_interpolant = interpolate.interp1d(scaledTorig, self.ys(), bounds_error=False, fill_value="extrapolate")
        y_new = y_interpolant(synthT)
        self.y = []
        for t, y in zip(synthT, y_new):
            self.y.append(TimeSample(t, y))

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