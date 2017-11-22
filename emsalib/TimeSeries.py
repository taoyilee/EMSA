import matplotlib
from .TimeSample import TimeSample
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, interpolate, fftpack

class TimeSeries:
    y : TimeSample = []
    ts = np.array([])
    ys = np.array([])

    def __init__(self, **kwargs):
        self.ts = np.array(kwargs.get('ts',[]))
        self.ys = np.array(kwargs.get('ys',[]))
        self.convertRaw()

    def zeroMean(self):
        self.ys = self.ys - np.mean(self.ys)
        self.convertRaw()

    def convertRaw(self):
        self.y = []
        for i in range(len(self.ts)):
            self.y.append(TimeSample(self.ts[i], self.ys[i]))

    def resample(self):
        fs = 33
        ps = 1 / fs
        n = np.int16(8192)
        freq = np.linspace(0, fs / 2, num=int(n // 2))
        ts_new = np.arange(min(self.ts), max(self.ts), ps)
        ys_interpolant = interpolate.interp1d(self.ts, self.ys)
        ys_new = ys_interpolant(ts_new)
        self.ts = ts_new
        self.ys = ys_new
        self.convertRaw()

    def plot(self, tstart=0, tend=None):
        plt.plot([yi.t for yi in self.y[tstart:tend]], [yi.y for yi in self.y[tstart:tend]])
        for yi in self.y[tstart:tend]:
            if yi.peak:
                plt.plot(yi.t, yi.y, 'ro', ms=5)
            if yi.valley:
                plt.plot(yi.t, yi.y, 'go', ms=5)
        plt.grid()

    def genRandom(self, length):
        self.ts = np.array(range(length))
        self.ys = np.array(np.random.randn(length))
        self.convertRaw()

    def __str__(self):
        return str(self.ts[0:10]) + str(self.ys[0:10])

    def setPeak(self, peak_idx):
        for i in peak_idx:
            self.y[i].setPeak()

    def setValley(self, valley_idx):
        for i in valley_idx:
            self.y[i].setValley()
