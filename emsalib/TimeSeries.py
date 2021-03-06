from emsalib.Signal import Signal
from .Motif import Motif
from .TimeSample import TimeSample

import numpy as np


class TimeSeries(Signal):

    def __init__(self, ts=[], ys=[], leftalign=True, offset=0, **kwargs):
        ts = np.array(ts)
        ys = np.array(ys)
        y = [TimeSample(t, y) for t, y in zip(ts, ys)]
        super().__init__(y, leftalign, offset)

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

    def motif(self, start=0, stop=None):
        return Motif(self.y[start:stop])

    def subseq(self, start=0, stop=None, leftalign=True, offset=0):
        return TimeSeries( ts=self.ts(start,stop), ys=self.ys(start,stop), leftalign=leftalign, offset=offset)
