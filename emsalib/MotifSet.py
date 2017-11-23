import matplotlib.pyplot as plt
from .Motif import Motif
import numpy as np


class MotifSet:
    motifs = []

    def __init__(self) :
        pass

    def append(self, motif):
        self.motifs.append(motif)

    def elasticRecale(self):
        aligned_motifs = []
        pts = 50
        synthT = list(range(2*pts))

        for m in self.motifs:
            if m.getFirstValley() is None:
                continue
            submotif0 = m.subseq(start=0, stop=m.findIdx(m.getFirstValley()))
            submotif0.mapSynthT(synthT[0:pts])
            submotif1 = m.subseq(start=m.findIdx(m.getFirstValley()))
            submotif1.mapSynthT(synthT[pts:])
            submotif0.concat(submotif1)
            aligned_motifs.append(submotif0)

        self.motifs = aligned_motifs

    def plot(self):
        for m in self.motifs:
            m.plot()

    def plotMean(self):
        meanMotif = [m.mean() for m in self.motifs]
        plt.hist(meanMotif)

    def plotVar(self):
        varMotif = [m.var() for m in self.motifs]
        plt.hist(varMotif)