import serial
import matplotlib.pyplot as plt

# Establish serial communication with the ESP32
serial_port = '/dev/cu.usbserial-210'  # Update with the correct serial port for your setup
baud_rate = 9600  # Update with the baud rate used by the ESP32
ser = serial.Serial(serial_port, baud_rate)

while True:
    # Read data from the serial port
    try:
      data = ser.readline().decode().strip()
      print(data)
    except:
          continue