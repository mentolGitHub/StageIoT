#include "BluetoothSerial.h"
#include <HardwareSerial.h>
#include <stdio.h>
#include <string.h>
#include <Arduino.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 2     
#define DHTTYPE DHT11

DHT_Unified dht(DHTPIN, DHTTYPE);


#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif


/* Déclaration des objets */

//ports séries
BluetoothSerial SerialBT;
HardwareSerial SerialPort(2); 

//variables de réception
String dataFromBluetooth;
String dataFromUart;
String timestamp, latitude, longitude, altitude, luminosite, vitesseAngulaireX, vitesseAngulaireY, vitesseAngulaireZ, pression, accelerationX, accelerationY, accelerationZ, angle, azimut;
String loraPayload, btPayload;
long distanceValue = 0;
float temperature, humidity;

/* Déclaration des fonctions */

void traitementReceptionBluetooth();
void traitementReceptionUart();
void dht_mesure(float* temperature, float* humidity);
const int triggerPin = 5; 
const int echoPin = 18; 


float distance();
bool is_ip_allowed = false;

uint32_t delayMS;

/* Initialisation */
void setup() 
{
  // Initialisation des communications
  Serial.begin(9600); //initialisation du port série
  SerialPort.begin(115200, SERIAL_8N1, 16, 17);  //initialisation de l'uart rx : 16 et tx : 17
  SerialBT.begin("Plateforme iot"); //initialisation du bluetooth
  
  // Initialisation des capteurs
  // capteur de température et d'humidité
  dht.begin();
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  Serial.println(F("------------------------------------"));
  Serial.println(F("Temperature Sensor"));
  Serial.print  (F("Sensor Type: ")); Serial.println(sensor.name);
  Serial.print  (F("Driver Ver:  ")); Serial.println(sensor.version);
  Serial.print  (F("Unique ID:   ")); Serial.println(sensor.sensor_id);
  Serial.print  (F("Max Value:   ")); Serial.print(sensor.max_value); Serial.println(F("°C"));
  Serial.print  (F("Min Value:   ")); Serial.print(sensor.min_value); Serial.println(F("°C"));
  Serial.print  (F("Resolution:  ")); Serial.print(sensor.resolution); Serial.println(F("°C"));
  Serial.println(F("------------------------------------"));
  // Print humidity sensor details.
  dht.humidity().getSensor(&sensor);
  Serial.println(F("Humidity Sensor"));
  Serial.print  (F("Sensor Type: ")); Serial.println(sensor.name);
  Serial.print  (F("Driver Ver:  ")); Serial.println(sensor.version);
  Serial.print  (F("Unique ID:   ")); Serial.println(sensor.sensor_id);
  Serial.print  (F("Max Value:   ")); Serial.print(sensor.max_value); Serial.println(F("%"));
  Serial.print  (F("Min Value:   ")); Serial.print(sensor.min_value); Serial.println(F("%"));
  Serial.print  (F("Resolution:  ")); Serial.print(sensor.resolution); Serial.println(F("%"));
  Serial.println(F("------------------------------------"));
  
  delayMS = sensor.min_delay / 1000;

  // capteur de distance
  pinMode(triggerPin, OUTPUT);
  pinMode(echoPin, INPUT);
  

  Serial.println("The device started, now you can pair it with bluetooth!");
}

/* Main loop */
void loop() 
{
  dht_mesure(&temperature, &humidity);
  traitementReceptionBluetooth();
  traitementReceptionUart();
  delay(delayMS);
}


/* Fonctions */

/**
 * @brief Traitement de la réception du bluetooth
 * 
 */
void traitementReceptionBluetooth()
{
  if (SerialBT.available()) {
    dataFromBluetooth = SerialBT.readString();
    Serial.println(dataFromBluetooth);
    
    char buffer[dataFromBluetooth.length() + 1];
    dataFromBluetooth.toCharArray(buffer, sizeof(buffer));
    char *token = strtok(buffer, ",");
    int i = 0;
    if (token != NULL) {
      switch (token[0]) {
        case '0':
          if(token[1] == '2'){
            switch (token[2])
            {
              case '1':
                is_ip_allowed = true;
                Serial.println("IP is allowed");
                break;

              case '0':
                is_ip_allowed = false;
                Serial.println("IP is not allowed");
                break;
            
              default:
                Serial.println("inconnu2 : " + token[2]);
                break;
            }
          }
          break;
        case '1':
          break;
        case 's':
          while (token != NULL) {
            switch (i) {
              case 0:
                break;
              case 1:
                timestamp = token;
                break;
              case 2:
                latitude = token;
                break;
              case 3:
                longitude = token;
                break;
              case 4:
                altitude = token;
                break;
              case 5:
                luminosite = token;
                break;
              case 6:
                vitesseAngulaireX = token;
                break;
              case 7:
                vitesseAngulaireY = token;
                break;
              case 8:
                vitesseAngulaireZ = token;
                break;
              case 9:
                pression = token;
                break;
              case 10:
                accelerationX = token;
                break;
              case 11:
                accelerationY = token;
                break;
              case 12:
                accelerationZ = token;
                break;
              case 13:
                angle = token;
                break;
              case 14:
                azimut = token;
                break;
              default:
                break;
            }
            token = strtok(NULL, ",");
            i++;
          }
          // envoi des data LoRa
          distanceValue = distance();
          loraPayload = "2" + timestamp + "," + latitude + "," + longitude + "," + altitude + "," + luminosite + "," + vitesseAngulaireX + "," + vitesseAngulaireY + "," + vitesseAngulaireZ + "," + pression + "," + accelerationX + "," + accelerationY + "," + accelerationZ + "," + angle + "," + azimut + "," + distanceValue + "," + String(humidity) + "," + String(temperature) + "\n";
          SerialPort.print(loraPayload);
          Serial.println("loraPayload : " + loraPayload);

          break;

        case '.':
          distanceValue = distance();
          char formattedDistance[6]; // 5 digits + null terminator
          snprintf(formattedDistance, sizeof(formattedDistance), "%05d", distanceValue);

          char formattedTemperature[6]; // 5 digits + null terminator
          snprintf(formattedTemperature, sizeof(formattedTemperature), "%05.2f", temperature);

          char formattedHumidity[6]; // 5 digits + null terminator
          snprintf(formattedHumidity, sizeof(formattedHumidity), "%05.2f", humidity);

          btPayload = "30" + String(formattedDistance) + "," + String(formattedTemperature) + "," + String(formattedHumidity) + "\n";
          SerialBT.print(btPayload);
          Serial.println("btPayload : " + btPayload);
          break;

        default:
          Serial.println("inconnu0 : " + token[0]);
          break;
      }
      
    }
  }
}

/**
 * @brief Traitement de la réception de l'UART
 * 
 */
void traitementReceptionUart()
{
  if (SerialPort.available()) {
    dataFromUart = SerialPort.readStringUntil('\n');
    Serial.print("UART : " + dataFromUart);
    //verifier le premier caractere
    switch (dataFromUart[0])
    {
      case '0':
        switch (dataFromUart[1])
        {
          case '1': //envoi du dev eui
            SerialBT.print(dataFromUart);
            break;
        }
        break;
      
      default:
        break;
    }
    Serial.write(dataFromUart.c_str());
    SerialBT.print(dataFromUart);
  }
}

/**
 * @brief Mesure la distance
 * 
 * @return float
 */
float distance(){
  //calcul de la distance avec le capteur hc sr04

  float duration, distance;

  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = (duration / 2) * 340/1000/10; 
  Serial.print("Distance: ");
  Serial.println(distance);
  return distance;
}

/**
 * @brief Mesure la température et l'humidité
 * 
 * @param temperature 
 * @param humidity
 *
 * @return void
 */
void dht_mesure(float* temperature, float* humidity){
  sensors_event_t event;
  dht.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    Serial.println(F("Error reading temperature!"));
  }
  else {
    Serial.print(F("Temperature: "));
    Serial.print(event.temperature);
    *temperature = event.temperature;
    Serial.println(F("°C"));
  }
  // Get humidity event and print its value.
  dht.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    Serial.println(F("Error reading humidity!"));
  }
  else {
    Serial.print(F("Humidity: "));
    Serial.print(event.relative_humidity);
    *humidity = event.relative_humidity;
    Serial.println(F("%"));
  }
}