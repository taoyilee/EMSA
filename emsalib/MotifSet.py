import matplotlib.pyplot as plt
from .Motif import Motif
import numpy as np


class MotifSet:
    motifs = []
    aligned_motifs = []

    def __init__(self):
        self.motifs = []
        self.aligned_motifs = []

    def append(self, motif):
        self.motifs.append(motif)

    def ElasticRecale(self):
        aligned_motifs = []
        for m in self.motifs:
            self.aligned_motifs.append(m)

    def plot(self):
        for m in self.motifs:
            m.plot()

    def plotMean(self):
        meanMotif = [m.getMean() for m in self.motifs]
        plt.hist(meanMotif)

    def plotVar(self):
        varMotif = [m.getVar() for m in self.motifs]
        plt.hist(varMotif)