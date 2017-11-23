from emsalib.Signal import Signal
from .TimeSample import TimeSample
import numpy as np


class TimeSeries(Signal):

    def __init__(self, ts=[], ys=[], **kwargs):
        ts = np.array(ts)
        ys = np.array(ys)
        y = [TimeSample(t, y) for t, y in zip(ts, ys)]
        super().__init__(y)

    def updateys(self, ysUpdate):
        self.y = [TimeSample(t, y) for t, y in zip(self.ts(), ysUpdate)]

    def genRandom(self, length):
        ts = np.array(range(length))
        ys = np.array(np.random.randn(length))
        self.y = [TimeSample(t, y) for t, y in zip(ts, ys)]

    def __str__(self):
        return str(self.ts()[0:10]) + str(self.ys()[0:10])

    def getPeaks(self):
        idx = []
        for i in range(len(self.y)):
            if self.y[i].peak:
                idx.append(i)

        return idx

    def getValleys(self):
        idx = []
        for i in range(len(self.y)):
            if self.y[i].valley:
                idx.append(i)

        return idx

    def setPeak(self, peak_idx):
        for i in peak_idx:
            self.y[i].setPeak()

    def setValley(self, valley_idx):
        for i in valley_idx:
            self.y[i].setValley()