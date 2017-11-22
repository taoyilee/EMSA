from .FilterMovingAvg import FilterMovingAvg


class FilterToolbox:
    flt_type = 'ma'
    filterLen = 5

    def __init__(self, type='ma',**kwargs):
        self.flt_type = type
        self.filterLen =  kwargs.get('filterLen',5)

    def filter(self, ts):
        if self.flt_type == 'ma':
            self.flt = FilterMovingAvg(self.filterLen)
            self.flt.filter(ts)