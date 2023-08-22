import ctypes
import numpy as np
from scipy.fftpack import fft
from picosdk.ps2000a import ps2000a as ps
from picosdk.functions import adc2mV, assert_pico_ok
import time
import matplotlib.pyplot as plt

# PicoScope settings
CHANNEL = ps.PS2000A_CHANNEL["PS2000A_CHANNEL_A"]
RANGE = ps.PS2000A_RANGE["PS2000A_2V"]
TIMEBASE = 4  # Timebase index
NUM_SAMPLES = 1000

# Open the PicoScope device
chandle = ctypes.c_int16()
status = {}
assert_pico_ok(ps.ps2000aOpenUnit(ctypes.byref(chandle), None, 1))

try:
    # Set up the channel
    assert_pico_ok(ps.ps2000aSetChannel(chandle, CHANNEL, 1, 1, RANGE))

    while True:
        # Collect time-domain data
        data = (ctypes.c_int16 * NUM_SAMPLES)()
        overflow = ctypes.c_int16()
        assert_pico_ok(
            ps.ps2000aGetValues(
                chandle,
                CHANNEL,
                ctypes.byref(data),
                ctypes.byref(overflow),
                TIMEBASE,
                NUM_SAMPLES,
                None,
            )
        )

        # Convert data to numpy array
        data_np = np.array(data)

        # Perform the FFT
        fft_result = fft(data_np)

        # Calculate the frequency components corresponding to the FFT result
        sampling_rate = 100000  # Replace with the actual sampling rate used for data acquisition
        freq_components = np.fft.fftfreq(NUM_SAMPLES, 1 / sampling_rate)

        # Find the maximum frequency component
        magnitude = np.abs(fft_result)
        max_index = np.argmax(magnitude)
        max_frequency = freq_components[max_index]

        # Print the peak frequency
        print(f"Peak frequency: {max_frequency} Hz")

        # Sleep for a short period to avoid overloading the CPU
        time.sleep(0.1)

finally:
    # Close the PicoScope device
    assert_pico_ok(ps.ps2000aCloseUnit(chandle))
