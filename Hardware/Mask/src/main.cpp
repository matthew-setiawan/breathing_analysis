#include <Wire.h>
#include "MAX30105.h"
#include <SPI.h>
 #include "FS.h"
#include "Adafruit_CCS811.h"
#include <Adafruit_Si7021.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Adafruit_Sensor.h>
#include <MPU6050.h>
#include <cmath>
#include <algorithm>
#include <string>

//Wi-FI
const char* ssid = "matthew";
const char* password = "123456789";

//Server
String serverip = "http://192.168.137.208:8000";
HTTPClient http;

//Sensors Initialization
Adafruit_CCS811 ccs;
MAX30105 heartSensor;
Adafruit_Si7021 tempSensor = Adafruit_Si7021();
MPU6050 imu;

volatile int beat = 0;

void interruptRoutine() {
  beat++;
}

String floatToString(float value) {
  char buf[10];
  dtostrf(value, 5, 2, buf);
  return String(buf);
}

void setup() {
  Serial.begin(9600);

  //Initialize WiFi
  WiFi.mode(WIFI_STA); // SETS TO STATION MODE!
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
      delay(1000);
      Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  //Initialize Bluetooth

  //Initialize SPI
  Wire.begin();
  SPI.begin();

  //Initialize MPU sensor
  imu.initialize();
  imu.CalibrateAccel();

  //Initialize C02 sensor
  ccs.begin();
  ccs.setDriveMode(CCS811_DRIVE_MODE_250MS);

  //Initialize Temp sensor
  tempSensor.begin();

  // Initialize MAX30102 sensor
  if (!heartSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("Could not find a valid MAX30102 sensor, check wiring!");
    while (1);
  }

  // Configure sensor settings
  heartSensor.setup(0, 4, 1, 2, 4096); // LED Pulse Width, ADC Range, Sample Rate, LED Current, Number of Samples
  heartSensor.setPulseAmplitudeRed(0x0A); // Turn Red LED to low to indicate sensor is running
  heartSensor.setPulseAmplitudeGreen(0); // Turn off Green LED

  // Start sensor readings
  heartSensor.enableDIETEMPRDY();

  attachInterrupt(0, interruptRoutine, FALLING);

}

void loop() {
  //CO2 SENSOR
  if (ccs.available()) {
    if (!ccs.readData()) {
      String url = serverip+"/datapost/MS3120001_"+floatToString(ccs.geteCO2());
      http.begin(url);
      int httpResponseCode = http.GET();
      String response = http.getString();
      http.end();
    }
  }

  //HEART SENSOR
  // Read sensor values
  int32_t irValue = heartSensor.getIR();
  int32_t redValue = heartSensor.getRed();
  float tempValue = heartSensor.readTemperature();

  //TEMPERATURE SENSOR
  float temperature = tempSensor.readTemperature();
  float humidity = tempSensor.readHumidity();

  // GYROSCOPE
  float ax = imu.getAccelerationX()/16000.0;
  float ay = imu.getAccelerationY()/16000.0;
  float az = imu.getAccelerationZ()/16000.0;
  float mag = sqrt(pow(ax,2) + pow(ay,2) + pow(az,2));

  // Send acceleration, heart rate and co2 data to server

  String url = serverip+"/datapost/MS3120001_"+floatToString(redValue)+"_"+floatToString(temperature)+"_"+floatToString(mag).substring(1);
  http.begin(url);//send <hr>-<co2>-<accmag>
  int httpResponseCode = http.GET();
  String response = http.getString();
  http.end();
}