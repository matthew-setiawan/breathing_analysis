import numpy as np
import matplotlib.pyplot as plt

# Define the parameters
amplitude = 1.0  # Amplitude of the sine waves
frequency = 2.0  # Frequency of the sine waves
noise_scale = [0.2, 0.5, 1, 2]  # Scale of the added noise
offsets = [0, 5, 10, 15]  # Distances in front of the mouth

# Generate x-axis values
x = np.linspace(0, 2 * np.pi, 50)

# Create subplots for each wave
fig, axs = plt.subplots(len(offsets), 1, figsize=(8, 6), sharex=True)

# Generate and plot the sine wave data with noise
for i, offset in enumerate(offsets):
    noise = noise_scale[i] * np.random.randn(len(x))
    y = amplitude * np.sin(frequency * x) + noise
    axs[i].plot(x, y)
    axs[i].set_yticks([])
    axs[i].set_ylabel("")
    axs[i].set_title(f"CO2 sensor readings in front of mouth d = {offset} cm")

# Customize the plot
plt.xlabel("Time")

# Adjust the spacing between subplots
plt.subplots_adjust(hspace=0.4)

# Show the plot
plt.savefig("co2readingvariations.png")
