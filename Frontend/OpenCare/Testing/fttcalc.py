import numpy as np

def calculate_fft(signal, sampling_rate):
    """
    Calculates the Fast Fourier Transform (FFT) of a signal.
    
    Args:
        signal (array-like): The input signal.
        sampling_rate (float): The sampling rate of the signal.
    
    Returns:
        tuple: A tuple containing the frequency values and the corresponding amplitudes.
    """
    n = len(signal)  # Length of the signal
    frequencies = np.fft.fftfreq(n, 1 / sampling_rate)  # Calculate the frequency values
    amplitudes = np.abs(np.fft.fft(signal))  # Calculate the FFT amplitudes
    
    return frequencies, amplitudes

