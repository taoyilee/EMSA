import matplotlib.pyplot as plt
from .TimeSample import TimeSample
import numpy as np


class Motif:
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

    def plot(self, tstart=0, tend=None):
        plt.plot([yi.t for yi in self.y[tstart:tend]], [yi.y for yi in self.y[tstart:tend]])
        for yi in self.y[tstart:tend]:
            if yi.peak:
                plt.plot(yi.t, yi.y, 'ro', ms=3)
            if yi.valley:
                plt.plot(yi.t, yi.y, 'go', ms=3)
                #plt.text(yi.t, yi.y, "u{:.1f}, v{:.1f}".format(self.getMean(), self.getVar()))

    def getFirstPeak(self):
        for yi in self.y:
            if yi.peak:
                return yi
        return None

    def getMean(self):
        return np.mean([yi.y for yi in self.y])

    def getVar(self):
        return np.var([yi.y for yi in self.y])
