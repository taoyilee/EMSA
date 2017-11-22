"""
compute the mean and stddev of 100 data sets and plot mean vs stddev.
When you click on one of the mu, sigma points, plot the raw data from
the dataset that generated the mean and stddev
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

alice = pd.read_csv('../datasets/filteredData/Alice.csv')
xs = np.array(alice['Time'])
ys = np.array(alice['Axis 1'])
keys1 = range(len(xs))
ptsdict = dict(zip(xs, ys))
fig = plt.figure(1)
line, = plt.plot(xs, ys, '-o', markersize = 2)
xlim_min = 0
xlim_delta = 5
xlim_max = xlim_delta
plt.xlim([xlim_min, xlim_max])
plt.ylim([-0.6, 0.6])

last_xidx = 0

def onpick(event, ptsdict, keys1,xlim_min, xlim_max, fig):
    xv = event.xdata
    yv = event.ydata
    xidx = np.abs(xs -xv).argmin()
    xidx_val = xs[xidx]
    pts_save = ptsdict.fromkeys(range(last_xidx, xidx))
    keys1 = keys1[xidx+1:]
    ptsdict = ptsdict.fromkeys(keys1)
    print(keys1)
    print(len(ptsdict))
    xlim_min = xidx_val
    xlim_max = xidx_val + 5
    fig.xlim([xlim_min, xlim_max])
    print("{} @ {} {}".format(xidx, xv, yv))

fig.canvas.mpl_connect('button_release_event', lambda event: onpick(event,
                                                                    ptsdict,
                                                                    keys1,xlim_min,
                                                                    xlim_max,
                                                                    fig))
plt.show()
