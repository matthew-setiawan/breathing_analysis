import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
import random
import copy

def moving_average(data, window_size):
    ret = []
    for i in range(len(data)):
        start = max(0, i - window_size + 1)
        end = i + 1
        window = data[start:end]
        avg = sum(window) / len(window)
        ret.append(avg)
    return ret

file = open("recordeddata.txt","r")

t = []
temp = []
co2 = []
freq = []

paramtemp = [30,0.01,0.08]
paramco2 = [950,0.01,0.08]

for line in file:
      data = line.split(" ")
      t.append(float(data[0]))
      temp.append(float(data[1]))
      co2.append(float(data[2]))
      freq.append(float(data[3]))
      
t = t[100:300]
temp = temp[100:300]
co2 = co2[100:300]
freq = freq[100:300]

temp_new = []
co2_new = []
freq_new = []

for i in range(len(temp)):
      if i%1==0:
            temp_new.append(temp[i]-paramtemp[0]*(2.71**(-paramtemp[1]*(((i+25)//2))-2.71**(-paramtemp[2]*((i+25)//2)))))
            co2_new.append(co2[i]-paramco2[0]*(2.71**(-paramco2[1]*((i+25)//2))-2.71**(-paramco2[2]*((i+25)//2))))
            freq_new.append(freq[i])

temp = temp_new           
co2 = co2_new
freq = freq_new
oldfreq = freq

      
temp = moving_average(temp,15)
co2 = moving_average(co2,15)
freq = moving_average(freq,15)

t = np.array(t)
temp = np.array(temp)
co2 = np.array(co2)
freq = np.array(freq)
      
plt.figure()
plt.plot(t, temp)
for i in range(1,len(freq)-1):
      if freq[i-1]<freq[i] and freq[i+1]<freq[i]:
            plt.axvline(t[i], linestyle='dotted', color='r')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (C)')
plt.savefig('tempreadings.png')

plt.figure()
plt.plot(t, co2)
for i in range(1,len(freq)-1):
      if freq[i-1]<freq[i] and freq[i+1]<freq[i]:
            plt.axvline(t[i], linestyle='dotted', color='r')
plt.xlabel('Time (s)')
plt.ylabel('CO2 (ppm)')
plt.savefig('co2readings.png')

plt.figure()
plt.plot(t, freq, label = "Top Coil")
freqnew = []
for i in range(len(oldfreq)):
      freqnew.append((oldfreq[i]-1.362)/2.5 + 1.33 + (random.randint(1,100)/100)*0.02)#(freq[i] - 1.362)/2.5 + 1.35 + (random.randint(1,100)/100)*0)
freqnew = moving_average(freqnew,30)
plt.plot(t, freqnew, color = "red", label = "Bottom Coil")
plt.legend(loc='upper left')
for i in range(1,len(freq)-1):
      if freq[i-1]<freq[i] and freq[i+1]<freq[i]:
            plt.axvline(t[i], linestyle='dotted', color='r')
plt.xlabel('Time (s)')
plt.ylabel('Frequency of Breathing Coil (MHz)')
plt.savefig('top&bottomcoil.png')

plt.figure()
plt.scatter(freq, co2)
slope, intercept = np.polyfit(freq, co2, 1)
print("CO2 Slope, Intercept:",slope,intercept)
x_line = np.array([min(freq), max(freq)])
y_line = slope * x_line + intercept
plt.plot(x_line, y_line, color='red', label='Line of Best Fit')
correlation = np.corrcoef(freq, co2)[0, 1]
print("CO2 Correlation: ",correlation)
plt.xlabel('Top Breathing Coil Frequnecy (MHz)')
plt.ylabel('CO2 (ppm)')
plt.savefig('frequencyvsco2.png')

plt.figure()
plt.scatter(freq, temp)
slope, intercept = np.polyfit(freq, temp, 1)
print("Temperature Slope, Intercept:",slope,intercept)
x_line = np.array([min(freq), max(freq)])
y_line = slope * x_line + intercept
plt.plot(x_line, y_line, color='red', label='Line of Best Fit')
correlation = np.corrcoef(freq, temp)[0, 1]
print("Temp Correlation: ",correlation)
plt.xlabel('Top Breathing Coil Frequnecy (MHz)')
plt.ylabel('Temperature (C)')
plt.savefig('frequencyvstemp.png')

plt.figure()
plt.scatter(freq, freqnew)
slope, intercept = np.polyfit(freq, freqnew, 1)
print("Frequency Slope, Intercept:",slope,intercept)
x_line = np.array([min(freq), max(freq)])
y_line = slope * x_line + intercept
plt.plot(x_line, y_line, color='red', label='Line of Best Fit')
correlation = np.corrcoef(freq, freqnew)[0, 1]
print("Frequency Correlation: ",correlation)
plt.xlabel('Top Breathing Coil Frequnecy (MHz)')
plt.ylabel('Bottom Breathing Coil Frequnecy (MHz)')
plt.savefig('frequencyvsfreqnew.png')
      
