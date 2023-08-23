## A Smart Breathing Mask for Breathing Training

A compilation of materials utilized in Final Year Project, "A Smart Breathing Mask for Breathing Training". The software for this project contained 3 main functional components: server, mask and knitted coil. The server contains functionality which stores device data and user data. The mask contains the ability to read CO2, temperature, heart rate and movements. The Knitted coil reads the resonant frequency of an inductor coil knitted around the users abdomen to track changes in breathing patterns. The follow gives the steps to sucessfully run the device.

## Step 1: Running the server

Visit Frontend/OpenCare\Website/
<b>Install the Packages</b>
````shell
pip3 install requirements.txt
````
<b>Option 1: Run server with free port number</b>
````shell
python3.9 manage.py runserver 0.0.0.0:8000
````
<b>Option 2: Run server with on the internet using web services</b>

## Step 2: Running the Smart Breathing Mask

Visit Hardware/Mask/src/main.cpp

<b>Edit the information to your WiFi username and password, and the IP of your computer/server</b>
````shell
// WiFi

const char* ssid = "matthew";
const char* password = "123456789";

//Server
String serverip = "http://192.168.137.168:8000";
````

<b>Run the files using platform.io or arduino IDE</b>

## Step 3: Running the Knitted Coil

Visit Hardware/Knitted\Coil/src/main.cpp

<b>Edit the information to your WiFi username and password, and the IP of your computer/server</b>
````shell
// WiFi

const char* ssid = "matthew";
const char* password = "123456789";

//Server
String serverip = "http://192.168.137.168:8000";
````

<b>Run the files using platform.io or arduino IDE</b>

## Step 4: Navigating the app

1. Create an account
2. Go to profile and add the device MS3120001
3. View that the device has been added in Devices
4. Click, and view the live data readings





