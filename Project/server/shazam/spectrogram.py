import numpy as np
from .cooleyTukey import FFT
import math

# Constants
dspRatio = 4
freqBinSize = 1024
maxFreq = 5000.0  # 5kHz
hopSize = freqBinSize // 32


class Peak:
    def __init__(self, time, freq):
        self.time = time  # Time in seconds
        self.freq = freq  # Frequency as complex number


# Spectrogram function to compute the spectrogram
def Spectrogram(sample, sample_rate):
    # Apply low-pass filter
    filtered_sample = LowPassFilter(maxFreq, sample_rate, sample)

    # Downsample the signal
    downsampled_sample = Downsample(filtered_sample, sample_rate, sample_rate // dspRatio)

    # Number of windows
    num_of_windows = len(downsampled_sample) // (freqBinSize - hopSize)
    spectrogram = []

    # Hamming window
    window = np.hamming(freqBinSize)

    # Perform STFT
    for i in range(num_of_windows):
        start = i * hopSize
        end = start + freqBinSize
        if end > len(downsampled_sample):
            end = len(downsampled_sample)

        bin_sample = np.zeros(freqBinSize)
        bin_sample[:end-start] = downsampled_sample[start:end]

        # Apply Hamming window
        bin_sample *= window

        # Compute FFT and store the result
        spectrogram.append(FFT(bin_sample))

    return spectrogram


# # Low-pass filter function
# def LowPassFilter(cutoff_frequency, sample_rate, input_signal):
#     nyquist = 0.5 * sample_rate
#     normal_cutoff = cutoff_frequency / nyquist
#     numtaps = 101  # Filter order
#     b = firwin(numtaps, normal_cutoff)
#     return lfilter(b, 1.0, input_signal)
# Dg

def LowPassFilter(cutoff_frequency, sample_rate, input_signal):
    rc = 1.0 / (2 * math.pi * cutoff_frequency)
    dt = 1.0 / sample_rate
    alpha = dt / (rc + dt)

    filtered_signal = []
    prev_output = 0.0

    for i, x in enumerate(input_signal):
        if i == 0:
            output = x * alpha
        else:
            output = alpha * x + (1 - alpha) * prev_output
        filtered_signal.append(output)
        prev_output = output

    return filtered_signal


# Downsample function
def Downsample(input_signal, original_sample_rate, target_sample_rate):
    if target_sample_rate <= 0 or original_sample_rate <= 0:
        raise ValueError("Sample rates must be positive")
    if target_sample_rate > original_sample_rate:
        raise ValueError("Target sample rate must be less than or equal to original sample rate")

    ratio = original_sample_rate // target_sample_rate
    if ratio <= 0:
        raise ValueError("Invalid ratio calculated from sample rates")

    resampled = []
    for i in range(0, len(input_signal), ratio):
        end = i + ratio
        if end > len(input_signal):
            end = len(input_signal)

        avg = np.mean(input_signal[i:end])
        resampled.append(avg)

    return resampled


# coef1=0.25
# coef2=0.25
import params
def ExtractPeaks(spectrogram, audio_duration):
    if len(spectrogram) < 1:
        return []

    # Frequency bands (logarithmic scale)
    bands = [(0, 10), (10, 20), (20, 40), (40, 80), (80, 160), (160, 512)]
    peaks = []
    bin_duration = audio_duration / len(spectrogram)

    # print(params.coef1)
    # print(params.coef2)
    cf1=params.coef1
    cf2=params.coef2
    for bin_idx, bin_sample in enumerate(spectrogram):
        max_mags = []
        max_freqs = []
        freq_indices = []

        for band in bands:
            band_min, band_max = band
            band_slice = bin_sample[band_min:band_max]

            # Find the strongest magnitude in the band
            max_mag = 0
            max_freq = 0
            freq_idx = 0

            for idx, freq in enumerate(band_slice):
                magnitude = abs(freq)
                if magnitude > max_mag:
                    max_mag = magnitude
                    max_freq = freq
                    freq_idx = band_min + idx

            max_mags.append(max_mag)
            max_freqs.append(max_freq)
            freq_indices.append(freq_idx)

        # Compute adaptive threshold
        mean_mag = np.mean(max_mags)
        std_mag = np.std(max_mags)
        adaptive_threshold = cf1*(mean_mag + cf2*std_mag)
        # adaptive_threshold = coef1*(mean_mag + coef2*std_mag)

        for i, value in enumerate(max_mags):
            if value > adaptive_threshold:
                peak_time_in_bin = freq_indices[i] * bin_duration / len(bin_sample)
                peak_time = bin_idx * bin_duration + peak_time_in_bin
                peaks.append(Peak(peak_time, max_freqs[i]))

    return peaks

