import numpy as np


def thresholdDetect(signal, threshold, win):
    if threshold < 0:
        out_idx = np.argwhere(signal < threshold)
        diff_idx = out_idx[1:]-out_idx[0:-1]
        winDur = win[0] + win[1]
        while len(np.argwhere(diff_idx <= winDur)) > 0:
            valid_idx = np.setdiff1d(range(0, len(out_idx)), np.argwhere(diff_idx <= winDur) + 1)
            out_idx = out_idx[valid_idx]
            diff_idx = out_idx[1:-1]-out_idx[0:-2]

        wf_before = win[0]
        wf_after = win[1]
        invalid_iwf = []
        valley_idx = []
        if out_idx[0] - wf_before >= 0 and out_idx[0] + wf_after < len(signal):
            start_idx = np.asscalar(out_idx[0] - wf_before)
            end_idx = np.asscalar(out_idx[0] + wf_after)
            wf_raw = signal[start_idx:end_idx]

        for iwf in range(1, len(out_idx)):
            if out_idx[iwf] - wf_before >= 0 and out_idx[iwf] + wf_after < len(signal):
                start_idx = np.asscalar(out_idx[iwf] - wf_before)
                end_idx = np.asscalar(out_idx[iwf] + wf_after)
                wf_raw = np.vstack((wf_raw, signal[start_idx:end_idx]))
                valley_idx = np.append(valley_idx,start_idx + np.argmin(signal[start_idx:end_idx]))
            else:
                invalid_iwf.append(iwf)
        out_idx = np.setdiff1d(out_idx, out_idx[invalid_iwf])
        return out_idx, wf_raw, valley_idx