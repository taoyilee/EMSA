from .TimeSeries import TimeSeries
from .Motif import Motif
from .MotifSet import MotifSet
from .FilterToolbox import FilterToolbox
import numpy as np
from scipy import signal


class SWM:
    flt = None
    filterLen = 5
    searchOrd = 5

    def __init__(self, flt_type='ma', **kwargs):
        self.filterLen = kwargs.get('filterLen', 5)
        self.searchOrd = kwargs.get('searchOrd', 5)
        self.flt = FilterToolbox(type=flt_type,filterLen=self.filterLen)

    def process(self, ts : TimeSeries ):
        ts.resample()
        ts.zeroMean()
        self.flt.filter(ts)
        self.labelPeakValley(ts)
        motifs =  self.MotifByPeaks(ts)
        motifs.elasticRecale()
        return motifs


    def labelPeakValley(self, ts : TimeSeries):
        peaks_idx = np.array(signal.argrelmax(ts.ys, order=self.searchOrd))[0]
        ts.setPeak(peaks_idx)
        valleys_idx = np.array(signal.argrelmin(ts.ys, order=self.searchOrd))[0]
        ts.setValley(valleys_idx)

    def MotifByPeaks(self, ts: TimeSeries):
        motifs = []
        peak_idx = ts.getPeaks()
        motifs = MotifSet()
        for i in range(len(peak_idx)-1):
            m = Motif(ts.y[peak_idx[i]:peak_idx[i + 1]])
            # dirty hack to remove unwanted motifs
            if m.getFirstPeak().y < 0.3:
                continue
            if abs(m.getVar()) < 0.1:
                continue
            if abs(m.getMean()) > 0.15:
                continue
            if abs(m.getVar()) > 0.35:
                continue
            motifs.append(m)
            
        return motifs

