from .TimeSeries import TimeSeries
from .MotifSet import MotifSet
from .FilterToolbox import FilterToolbox
import matplotlib.pyplot as plt
import numpy as np


class SWM:
    flt = None
    filterLen = 5
    searchOrd = 15
    distThres = 5
    minLen = 40
    maxLen = 150
    searchRange = 10

    def __init__(self, flt_type='ma', distThres=0.075, minLen=50, maxLen=51, searchRange=10, searchOrd=15, filterLen=5):
        self.filterLen = filterLen
        self.searchOrd = searchOrd
        self.distThres = distThres
        self.minLen = minLen
        self.maxLen = maxLen
        self.searchRange = searchRange
        self.flt = FilterToolbox( type=flt_type, filterLen=self.filterLen )

    def processVerbose(self, ts: TimeSeries):
        ts.resample()
        ts.zeroMean()
        self.flt.filter( ts )
        fom = -1
        motifs = []
        meanErr = []
        droppedPts = []
        distList = []

        for curLen in range( self.minLen, self.maxLen ):
            print( "Total length {} / {} = {}".format( len( ts ), curLen, len( ts ) // curLen ) )
            for i in range( len( ts ) // curLen ):
                tsTemplate = ts.subseq( start=i * curLen, stop=i * curLen + curLen )
                if i == 0:
                    tsSeg1 = ts.subseq( start=i * curLen + curLen, leftalign=True, offset=-tsTemplate.duration() )
                else:
                    tsSeg1 = ts.subseq( start=0, stop=i * curLen )
                    tsSeg2 = ts.subseq( start=i * curLen + curLen, leftalign=False, offset=-tsTemplate.duration() )
                    tsSeg1.concat( tsSeg2 )
                (motifsi, meanErri, droppedPtsi, distListi) = self.searchByTemplate( tsSeg1, tsTemplate )
                fom_cur = len( motifsi ) / (meanErri * droppedPtsi)
                if fom_cur > fom:
                    fom = fom_cur
                    motifs = motifsi
                    meanErr = meanErri
                    droppedPts = droppedPtsi
                    distList = distListi
                    print(
                        "(Pocket Updated {:.3f}) Found {} motifs, mean Dist = {:.4f}, dropped {} points in original TS".format(
                            fom, len( motifs ), meanErr,
                            droppedPts ) )
                else:
                    print(
                        "Found {} motifs, mean Dist = {:.4f}, dropped {} points in original TS".format( len( motifs ),
                                                                                                        meanErr,
                                                                                                        droppedPts ) )
        return motifs, meanErr, droppedPts, distList

    def process(self, ts: TimeSeries):
        ts.resample()
        ts.zeroMean()
        self.flt.filter( ts )
        fom = -1
        motifs = []
        meanErr = []
        droppedPts = []
        distList = []

        for curLen in range( self.minLen, self.maxLen ):
            for i in range( len( ts ) // curLen ):
                tsTemplate = ts.subseq( start=i * curLen, stop=i * curLen + curLen )
                if i==0:
                    tsSeg1 = ts.subseq( start=i * curLen + curLen, leftalign=True, offset=-tsTemplate.duration())
                else:
                    tsSeg1 = ts.subseq( start=0, stop=i * curLen )
                    tsSeg2 = ts.subseq( start=i * curLen + curLen, leftalign=False, offset=-tsTemplate.duration() )
                    tsSeg1.concat( tsSeg2 )
                (motifsi, meanErri, droppedPtsi, distListi) = self.searchByTemplate( tsSeg1, tsTemplate )
                fom_cur = len(motifsi)/(meanErri*droppedPtsi)
                if fom_cur > fom:
                    fom = fom_cur
                    motifs = motifsi
                    meanErr = meanErri
                    droppedPts = droppedPtsi
                    distList = distListi

        return motifs, meanErr, droppedPts, distList

    def searchByTemplate(self, ts, tsTemplate):
        distList = []
        templateLen = len( tsTemplate )
        pts = int( len( tsTemplate ) * (100 + self.searchRange) / 100 )
        tsTemplate.mapSynthT( range( pts ) )
        motifs = MotifSet()
        motifs.append( tsTemplate.motif() )
        ErrList = []
        droppedPts = 0
        while len( ts ) > int( templateLen * (100 + self.searchRange) / 100 ) :
            for candLen in range( int( templateLen * (100 - self.searchRange) / 100 ),
                                  int( templateLen * (100 + self.searchRange) / 100 ) ):
                tsCandidate = ts.subseq( start=0, stop=candLen )
                tsCandidate.mapSynthT( range( pts ) )
                dist = tsTemplate.euclideanDist( tsCandidate )
                distList.append( dist )
                if dist < self.distThres:
                    ErrList.append(dist)
                    m = tsCandidate.motif()
                    motifs.append( m )
                    ts = ts.subseq( start=candLen )
                    break
            ts = ts.subseq( start=1 )
            droppedPts +=1

        meanErr = np.mean(ErrList)
        return (motifs, meanErr, droppedPts, distList)
