
import numpy as np

# FFT computes the Fast Fourier Transform (FFT) of the input data,
# converting the signal from the time domain to the frequency domain.
# Using numpy's FFT implementation for simplicity
def FFT(input):
    complex_array = np.array(input, dtype=complex)

    fft_result = np.copy(complex_array)
    return recursive_fft(fft_result)

def recursive_fft(complex_array):
    N = len(complex_array)
    if N <= 1:
        return complex_array

    even = complex_array[::2]
    odd = complex_array[1::2]

    even = recursive_fft(even)
    odd = recursive_fft(odd)

    fft_result = np.zeros(N, dtype=complex)
    for k in range(N // 2):
        t = np.exp(-2j * np.pi * k / N)
        fft_result[k] = even[k] + t * odd[k]
        fft_result[k + N // 2] = even[k] - t * odd[k]

    return fft_result

# # Example usage
# input_signal = [0.0, 1.0, 0.0, -1.0]  # A simple test signal
# fft_output = FFT(input_signal)
# print(fft_output)
