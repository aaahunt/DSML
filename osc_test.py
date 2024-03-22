import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

# Example data generation (replace with your gyroscopic data)
t = np.linspace(0, 20, 1000)  # Time from 0 to 20 seconds
data = 2 * np.sin(2 * np.pi * t / 5)  # Example data oscillating between -2 and 2

# Detect peaks and troughs
peaks, _ = find_peaks(data, height=1.5)  # Peaks with height > 0
troughs, _ = find_peaks(-data, height=-1.5)  # Troughs in the inverted data

# Labeling cycles (example: from peak to peak)
cycle_labels = np.zeros(len(data))
for i in range(len(peaks) - 1):
    cycle_labels[peaks[i]:peaks[i+1]] = i+1

# Plotting the data with cycle labels
plt.figure(figsize=(10, 6))
plt.plot(t, data, label='Gyroscopic Data')
plt.scatter(t[peaks], data[peaks], color='red', label='Peaks')
plt.scatter(t[troughs], data[troughs], color='green', label='Troughs')
for i in range(len(peaks) - 1):
    plt.fill_between(t[peaks[i]:peaks[i+1]], data[peaks[i]:peaks[i+1]], alpha=0.2, label=f'Cycle {i+1}')
plt.legend()
plt.xlabel('Time (seconds)')
plt.ylabel('Gyroscopic Reading')
plt.title('Gyroscopic Data Oscillation and Cycle Labeling')
plt.show()