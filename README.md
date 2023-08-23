## A Smart Breathing Mask for Breathing Training

A compilation of materials utilized in Final Year Project, "A Smart Breathing Mask for Breathing Training". The software for this project contained 3 main functional components: server, mask and knitted coil. The server contains functionality which stores device data and user data. The mask contains the ability to read CO2, temperature, heart rate and movements. The Knitted coil reads the resonant frequency of an inductor coil knitted around the users abdomen to track changes in breathing patterns.

#How to use?

There are three core software used in this project: web application, software for knitted coil and software for mask.

<h2>Step 1: Running web application</h2>h2>
- Install Django and Python3.9
- Run python3.9 manage.py runserver 0.0.0.0:8000 to run it on your local internet connection

#Step 2: Modifying the hardware to connect to the server
- Check your IP and change the source code (main.cpp) for both hardware. Modify the address to your IP

#Step 3: Visit the website
- Create a user and link the device code to your account
- View the live readings for your device on the web application





