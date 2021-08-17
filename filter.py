import numpy as np
from scipy.signal import butter,filtfilt# Filter requirements.
import os
import sys
import matplotlib.pyplot as plt

fs = 30000.0       # sample rate, Hz
cutoff = [300 , 3000]     # desired cutoff frequency of the filter, Hz 
nyq = 0.5 * fs  # Nyquist Frequencyorder = 2 

def butter_lowpass_filter(data, cutoff, fs, order):
	normal_cutoff = cutoffw / nyq
	# get the filter coefficients
	b, a = butter (order, normal_cutoff, btype = 'bandpass', analog = False)
	y = filtfile(b, a, data)
	return y


def _kernelGaussian(size=100, sigma=None):
    """
    Return a 1d array shaped like a Gaussian curve with area of 1.
    Optionally provide a sigma (the larger, the wider the curve).
    """
    if not sigma:
        sigma = size/7
    points = np.arange(int(size))
    points = np.exp(-np.power(points-size/2, 2) / (2*np.power(sigma, 2)))
    points = points/sum(points)
    return points


def _convolve(data, kernel):
    """
    Convolve the data with the kernel. The edges of the returned data (half the
    size of the kernel) will be nan. If you want a different convolution method,
    code it yourself!
    """
    smooth = np.convolve(data, kernel, mode='valid')
    nansNeeded = int((len(data)-len(smooth))/2)
    smooth = np.concatenate((np.full(nansNeeded, np.nan), smooth))
    nansNeeded = int(len(data)-len(smooth))
    smooth = np.concatenate((smooth, np.full(nansNeeded, np.nan)))
    return smooth


def remove(abf):
    """
    Revert to the original data in the ABF. This is accomplished by opening
    the original file and re-reading the data (into abf.data).
    """
    with open(abf.abfFilePath, 'rb') as fb:
        abf._loadAndScaleData(fb)


def gaussian(abf, sigmaMs=5, channel=0):
    """
    Perform a gaussian convolution on every sweep of the indicated channel.
    Note that this performs smoothing once (acting directly on abf.data), and
    subsequent calls will keep smoothing the smoothed trace.

    Set sigmaMs to 0 or False to remove the filter.
    """
    if not "data" in dir(abf):
        abf.setSweep(0)
    if sigmaMs:
        pointsPerMs = abf.dataRate/1000.0
        kernel = _kernelGaussian(int(pointsPerMs*sigmaMs*7))
        abf.data[channel] = _convolve(abf.data[channel], kernel)
    else:
        remove(abf)
