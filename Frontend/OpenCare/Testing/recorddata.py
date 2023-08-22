import extfunctions
import time

data = ""
timestamp = 0.1
device = "MS3120001"
t = 0

for i in range(1200):
      if i%10==0:
            print(i)
      data = data + str(t) + ' ' + extfunctions.getreading(device,"temperaturereading") + ' ' + extfunctions.getreading(device,"co2reading") + ' ' + extfunctions.getreading(device,"knittedcoilarea1") + '\n'
      time.sleep(timestamp)
      t = t + timestamp
      
file = open('recordeddata.txt','w')

file.write(data)

file.close()
