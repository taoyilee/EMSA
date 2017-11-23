from emsalib.Signal import Signal

class Motif(Signal):

    def __init__(self, y):
        super().__init__(y)

    def getFirstPeak(self):
        for yi in self.y:
            if yi.peak:
                return yi
        return None


    def getFirstValley(self):
        for yi in self.y:
            if yi.valley:
                return yi
        return None

    def subseq(self, start=0, stop=None):
        return Motif(self.y[start:stop])