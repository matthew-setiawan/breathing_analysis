import pyautogui
from PIL import Image
import pytesseract
import requests
import extfunctions
import numpy as np

url = "http://172.27.160.198:8000"
device = "MS3120001"

def calculate_average(arr):
    total = sum(arr)
    average = total / len(arr)
    return average

def monitor_screen(region):
      dataprev = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
      tempparam = [18,5]
      co2param = [1252,-188]
      
      #Train Data
      coil = []
      temp = []
      co2 = []
      
      #PrevVal
      tempprev = 0
      co2prev = 0
      
      while True:
            # Capture screenshot of the specified region
            screenshot = pyautogui.screenshot(region=region)
            
            # Convert the screenshot to grayscale
            grayscale_image = screenshot.convert("L")
            # Perform OCR on the grayscale image
            ocr_text = pytesseract.image_to_string(grayscale_image)
            ocr_text = ocr_text.replace("\n"," ")
            data = ocr_text.split(" ")
            for i in range(len(data)):
                  if data[i]=='at':
                        try:
                              #Print Gotten Data
                              print("Coil: ",data[i+1])
                              requests.get(url+"/datapost/MS3120001_"+data[i+1]+"_"+data[i+1])
                              
                              #Moving Average
                              ave = calculate_average(dataprev)
                              requests.get(url+"/datapost/MS3120001_"+str(ave*tempparam[0]+tempparam[1])+"_"+str(ave*tempparam[0]+tempparam[1])+"_"+str(ave*co2param[0]+co2param[1])+"_"+str(ave*co2param[0]+co2param[1]))
                              dataprev = dataprev[1:]
                              dataprev.append(float(data[i+1]))
                              
                              #Update Train Data and Param
                              temperaturereading = float(extfunctions.getreading(device,"temperaturereading"))
                              co2reading = float(extfunctions.getreading(device,"co2reading"))
                              if temperaturereading!=tempprev and co2reading!=co2prev:
                                    if len(coil)==50:
                                          coil = coil[1:]
                                          temp = temp[1:]
                                          co2 = co2[1:]
                                          coil.append(float(data[i+1]))
                                          temp.append(temperaturereading)
                                          co2.append(co2reading)
                                    else:
                                          coil.append(float(data[i+1]))
                                          temp.append(temperaturereading)
                                          co2.append(co2reading)
                                    tempparam[0], tempparam[1] = np.polyfit(coil, temp, 1)
                                    co2param[0], co2param[1] = np.polyfit(coil, co2, 1)
                                    print("Temp Param:",tempparam)
                                    print("C02 Param:",co2param)
                                    print(len(coil))
                                    tempprev = temperaturereading
                                    co2prev = co2reading
                        except:
                              continue
                  else:
                        requests.get(url+"/datapost/MS3120001_"+data[i+1]+"_"+data[i+1])       
        
# Specify the region to monitor (coordinates of top-left and bottom-right points)
region_to_monitor = (240, 1130, 360, 1145)  # Example values, adjust as per your requirements

# Start monitoring the screen region and continuously print OCR contents
monitor_screen(region_to_monitor)