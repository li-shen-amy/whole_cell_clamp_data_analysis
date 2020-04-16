import pyabf
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
import os

def plot_oriabf(abf_filename, plt_show, save_fig, save_mat):
    abf = pyabf.ABF((abf_filename+'.abf'))
    led = np.zeros([len(abf.sweepList), len(abf.sweepD(3))])
    stim_bound = np.zeros([len(abf.sweepList),2])
    fig = plt.figure(figsize=(8, 5))
    nsweep = len(abf.sweepList)
    savemat = {}
    for sweep_num in abf.sweepList:
        abf.setSweep(sweep_num)
        led_tmp = abf.sweepD(3)
        led[sweep_num] = led_tmp
        t1 = first_exceed_index(led_tmp, 0)
        t2 = last_exceed_index(led_tmp, 0)

        # plot the ADC (voltage recording)
        ax1 = fig.add_subplot(nsweep, 1, sweep_num + 1)
        ax1.set_title('Sweep' + str(sweep_num + 1))
        ax1.plot(abf.sweepX, abf.sweepY)
        ax1.set_ylabel(abf.sweepLabelY)

        # if len(abf.sweepEpochs.p1s) > 2:
        #     epochNumber = 2
        #     t1 = abf.sweepEpochs.p1s[epochNumber] * abf.dataSecPerPoint
        #     t2 = abf.sweepEpochs.p2s[epochNumber] * abf.dataSecPerPoint
        #     plt.axvspan(t1, t2, color='r', alpha=.3, lw=0)
        #     plt.grid(alpha=.2)
        #
        # if len(abf.sweepEpochs.p1s) > 3:
        #     epochNumber = 3
        #     t1 = abf.sweepEpochs.p1s[epochNumber] * abf.dataSecPerPoint
        #     t2 = abf.sweepEpochs.p2s[epochNumber] * abf.dataSecPerPoint
        #     plt.axvspan(t1, t2, color='g', alpha=.3, lw=0)
        #     plt.grid(alpha=.2)

        if t1 >= 0 and t2 >= 0:
            plt.axvspan(abf.sweepX[t1], abf.sweepX[t2], color='g', alpha=.3, lw=0)
            plt.grid(alpha=.2)

        stim_bound[sweep_num][0] = t1
        stim_bound[sweep_num][1] = t2

        # plot the DAC (clamp current)
        # ax2 = fig.add_subplot(nsweep+1, 1, nsweep+1)
        # ax2.set_title("LED")
        # ax2.plot(abf.sweepX, abf.sweepD(3), color='r')
        # ax2.set_yticks([0, 1])
        # ax2.set_yticklabels(["OFF", "ON"])
        # ax2.axes.set_ylim(-.5, 1.5)
        # ax2.set_xlabel(abf.sweepLabelX)

    plt.show(block=plt_show)
    if save_fig:
        plt.savefig(os.path.join(abf_filename + '.png'))
    plt.close()
    if save_mat:
        savemat['led_stim'] = led
        savemat['stim_bound'] = stim_bound
        scipy.io.savemat(os.path.join(abf_filename + '_LED.mat'), dict(savemat))
    print('Loading Done')


def first_exceed_index(signal, threshold):
    idx = 0
    while idx < len(signal):
        s = signal[idx]
        if s > threshold:
            return idx
        idx += 1
    return -1


def last_exceed_index(signal, threshold):
    idx = len(signal)-1
    while idx >= 0:
        s = signal[idx]
        if s > threshold:
            return idx
        idx -= 1
    return -1