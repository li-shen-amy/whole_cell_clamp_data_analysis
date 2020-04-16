import pyabf
import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.io
from SubtractBaseline import removeBaseline

abf_path = 'C:\\Users\\zhanglab419\\Dropbox\\MS_Gaba_reward\\MS SOM rebound'
abf_file = '2020_01_14_0027.abf'

[filename, file_extension] = os.path.splitext(abf_file)
abf = pyabf.ABF(os.path.join(abf_path, abf_file))
fig = plt.figure(figsize=(8, 5))
nsweep = len(abf.sweepList)
lenSig = len(abf.sweepY)

winDur = 10000
ifplot = 0
processed_signal = np.empty([nsweep, lenSig])
for sweep_num in abf.sweepList:
    abf.setSweep(sweep_num)
    signal = abf.sweepY
    processed_signal[sweep_num], _ = removeBaseline(signal, winDur, ifplot)

    ax1 = fig.add_subplot(nsweep, 1, sweep_num + 1)
    ax1.set_title('Sweep' + str(sweep_num + 1))
    ax1.plot(abf.sweepX, processed_signal[sweep_num])
    ax1.set_ylabel(abf.sweepLabelY)

plt.show(block=False)
plt.savefig(os.path.join(abf_path, filename + '_baselineRemoved.png'))
plt.close()
scipy.io.savemat(os.path.join(abf_path, filename + '_baselineRemoved.mat'), dict(processed_signal=processed_signal))