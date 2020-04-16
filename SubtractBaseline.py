import pyabf
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import math


def removeBaseline(signal, winDur, ifplot):
    baseline = np.empty(math.floor(len(signal)/winDur)+1)
    for epoch in range(0, math.floor(len(signal)/winDur)):
        baseline[epoch] = np.mean(signal[epoch*winDur:epoch*winDur+winDur-1])
    baseline = baseline[:-2]
    end_point = int((math.floor(len(signal)/winDur)-1)*winDur+winDur/2)
    x = np.linspace(winDur/2, end_point, num=math.floor(len(signal)/winDur)-1, endpoint=True)
    f = interp1d(x, baseline)
    x = np.append(0, x)
    x = np.append(x, len(signal))
    baseline = np.append(baseline[0], baseline)
    baseline = np.append(baseline, baseline[-1])

    xnew = np.array(range(int(winDur/2), end_point + 1))
    ynew = f(xnew)
    xnew = np.append(np.array(range(0, int(winDur/2))), xnew)
    xnew = np.append(xnew, np.array(range(end_point + 1, len(signal))))
    ynew = np.append(np.tile(baseline[0], int(winDur/2)), ynew)
    ynew = np.append(ynew, np.tile(baseline[-1],  len(signal) - end_point - 1))
    xnew = xnew.astype('float')
    processed_signal = signal-ynew

    if ifplot:
        fig = plt.figure(figsize=(8, 5))
        ax1 = fig.add_subplot(2, 1, 1)
        ax1.plot(xnew, signal, '-')
        ax1.plot(xnew, ynew, 'r-')
        ax1.set_title('Orignal Signal')
        ax1.legend(['Original', 'Baseline'], loc='best')

        ax2 = fig.add_subplot(2, 1, 2)
        ax2.plot(xnew, processed_signal, '-')
        ax2.plot(xnew[[0, -1]], [0, 0], 'r')
        ax2.set_title('Baseline Removed')
        plt.show()

    return processed_signal, ynew