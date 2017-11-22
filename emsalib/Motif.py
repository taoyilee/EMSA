import matplotlib.pyplot as plt
import numpy as np


class Motif:
    xs = []
    ys = []

    def __init__(self, xs, ys):
        self.xs = xs - min(xs)
        self.ys = ys

    def plot(self):
        plt.plot(self.xs, self.ys)
