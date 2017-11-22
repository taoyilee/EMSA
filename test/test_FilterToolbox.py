import unittest
import emsalib as emsa
import copy


class FilterMATest(unittest.TestCase):
    def setUp(self):
        self.flt = emsa.FilterMovingAvg(filterLen=5)
        self.ts = emsa.TimeSeries()
        self.ts.genRandom(100)

    def test_filterKeeptLength(self):
        self.tsnoisy = copy.copy(self.ts)
        self.flt.filter(self.ts)
        self.assertEqual(len(self.tsnoisy.ts), len(self.ts.ts))

    def test_filterKeepyLength(self):
        self.tsnoisy = copy.copy(self.ts)
        self.flt.filter(self.ts)
        self.assertEqual(len(self.tsnoisy.ys), len(self.ts.ys))

    def test_filterChangedyValue(self):
        self.tsnoisy = copy.copy(self.ts)
        self.flt.filter(self.ts)
        self.assertTrue(sum(abs(self.tsnoisy.ys - self.ts.ys)) !=0)

if __name__ == '__main__':
    unittest.main()
