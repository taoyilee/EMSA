class TimeSample:
    t = 0.0
    y = 0.0
    peak = False
    valley = False
    def __init__(self, t, y):
        self.t  = t
        self.y = y