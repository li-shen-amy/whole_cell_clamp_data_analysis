import scipy.io
from thresholdDetect import thresholdDetect
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

abf_path = 'C:\\Users\\zhanglab419\\Dropbox\\MS_Gaba_reward\\MS SOM rebound\\'
save_name = '2020_01_14_0027_baselineRemoved'
# file_name = 'C:\\Users\\zhanglab419\\Dropbox\\MS_Gaba_reward\\MS SOM rebound\\2020_01_14_0027_baselineRemoved.mat'
file_name = os.path.join(abf_path, save_name)
led_name = '2020_01_14_0027_LED'

signal_mat = scipy.io.loadmat(file_name)
led_mat = scipy.io.loadmat(os.path.join(abf_path, led_name))

threshold_detected = {}
cross_idx_all = []
wf_detect_all = []
valley_idx_all = []
hist_spk_all = []
for sweep_num in range(0, 4):
    signal_todo = signal_mat['processed_signal'][sweep_num]
    cross_idx, wf_detect, valley_idx = thresholdDetect(signal_todo, -30, [4, 16])
    histbin = np.array(range(0, len(signal_todo), 1000))
    hist_spk, _ = np.histogram(valley_idx, bins=histbin)
    fig = plt.figure(figsize=(8, 5))
    ax1 = fig.add_subplot(4, 1, 1)
    for idx in valley_idx:
        ax1.plot(histbin[:-1] + 500, hist_spk, 'k-')
    ax1.plot(led_mat['led_stim'][sweep_num], 'r')
    ax1.set(xlim=(0, len(signal_todo)-1))

    ax2 = fig.add_subplot(4, 1, 2)
    for idx in valley_idx:
        ax2.plot(np.tile(idx, 2), [0, 1], 'k-')
    ax2.plot(led_mat['led_stim'][sweep_num], 'r')
    ax2.set(xlim=(0, len(signal_todo)-1))

    ax3 = fig.add_subplot(4, 1, 3)
    ax3.plot(signal_todo)
    ax3.plot(led_mat['led_stim'][sweep_num], 'r')
    ax3.set(xlim=(0, len(signal_todo)-1))

    ax4 = fig.add_subplot(4, 2, 8)
    ax4.plot(np.transpose(wf_detect))

    plt.show(block=False)
    plt.savefig(os.path.join(abf_path, save_name + '_thresholdDetect_' + str(sweep_num) + '.png'))
    plt.close()

    cross_idx_all.append(cross_idx)
    wf_detect_all.append(wf_detect)
    valley_idx_all.append(valley_idx)
    hist_spk_all.append(hist_spk)

threshold_detected['cross_idx'] = cross_idx_all
threshold_detected['wf_detect'] = wf_detect_all
threshold_detected['valley_idx'] = valley_idx_all
threshold_detected['hist_spk'] = hist_spk_all

scipy.io.savemat(os.path.join(abf_path, save_name + '_thresholdDetect.mat'), dict(threshold_detected))