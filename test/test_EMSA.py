import unittest
import emsalib as emsa
import copy


class EMSATest(unittest.TestCase):
    def setUp(self):
        self.emsa = emsa.EMSA(flt_type='ma', filterLen=5)
        self.ts = emsa.TimeSeries()
        self.ts.genRandom(100)

    def test_filterKeeptLength(self):
        self.tsnoisy = copy.copy(self.ts)
        self.emsa.process(self.ts)
        self.assertEqual(len(self.tsnoisy.ts), len(self.ts.ts))

    def test_filterKeepyLength(self):
        self.tsnoisy = copy.copy(self.ts)
        self.emsa.process(self.ts)
        self.assertEqual(len(self.tsnoisy.ys), len(self.ts.ys))

    def test_filterChangedyValue(self):
        self.tsnoisy = copy.copy(self.ts)
        self.emsa.process(self.ts)
        self.assertTrue(sum(abs(self.tsnoisy.ys - self.ts.ys)) !=0)

if __name__ == '__main__':
    unittest.main()
