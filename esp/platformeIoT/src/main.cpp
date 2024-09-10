#include "BluetoothSerial.h"
#include <HardwareSerial.h>
#include <stdio.h>
#include <string.h>
#include <Arduino.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <thread>
#include <Stream.h>

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
long distanceValue = 0;
float temperature, humidity;

const int triggerPin = 5; 
const int echoPin = 18; 
uint32_t delayMS;

bool is_ip_allowed = false;

/* Déclaration des fonctions */

void traitementReceptionBluetooth();
void traitementReceptionUartLoPy();
void traitementReceptionUartJetson();
void donneesCapteurs();
void dht_mesure(float* temperature, float* humidity);
float distance();


/* Initialisation */
void setup() 
{
  // Initialisation des communications
  Serial.begin(115200); //initialisation du port série (qui fait aussi la communication avec la jetson)
  SerialPort.begin(115200, SERIAL_8N1, 16, 17);  //initialisation de l'uart rx : 16 et tx : 17 (pour l'emetteur LoRa)
  SerialBT.begin("Plateforme iot"); //initialisation du bluetooth (pour la communicaiton avec le téléphone)


  
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

  std::thread t([&]() { dht_mesure(&temperature, &humidity); });
  t.detach();
  
  delayMS = sensor.min_delay / 1000;

  // capteur de distance
  pinMode(triggerPin, OUTPUT);
  pinMode(echoPin, INPUT);
  

  Serial.println("The device started, now you can pair it with bluetooth!");
}

/* Main loop */
void loop() 
{
  traitementReceptionBluetooth();
  traitementReceptionUartLoPy();
  traitementReceptionUartJetson();
}


/* Fonctions */

/**
 * @brief Forward des données bluetooth vers la Jetson
 * 
 */
void traitementReceptionBluetooth()
{
  if (SerialBT.available()) {
    dataFromBluetooth = SerialBT.readString();
    char buffer[dataFromBluetooth.length() + 1];
    dataFromBluetooth.toCharArray(buffer, sizeof(buffer));
    char *token = strtok(buffer, ",");
    int i = 0;
    if (token != NULL) {
      if (token[0] == '0') { 
        if(token[1] == '2') {
          if(token[2] == '1'){
            is_ip_allowed = true;
          }
          else if(token[2] == '0'){
            is_ip_allowed = false;
          }
        }
      }
    }

    Serial.write((dataFromBluetooth + "\n").c_str());
  }
}

/**
 * @brief Forward des données de la LoPy vers la Jetson
 * 
 */
void traitementReceptionUartLoPy()
{
  if (SerialPort.available()) {
    dataFromUart = SerialPort.readStringUntil('\n');    
    Serial.write(("LoRa"+dataFromUart+"\n").c_str());
    SerialBT.print(dataFromUart);
  }
}

/**
 * @brief Traitement de la reception de l'uart de la Jetson
 * 
 */
void traitementReceptionUartJetson()
{
  dataFromUart = "";
  if (Serial.available()) {
    dataFromUart = Serial.readStringUntil('\n');
    // choisir si l'on envoit en LoRa ou via la connection du téléphone
    if (is_ip_allowed) {
      SerialBT.print(dataFromUart);
    }
    else {
      SerialPort.print(dataFromUart+"\n");
    }
  }
}

/**
 * @brief forward des données des capteurs vers la Jetson
 * 
 */

void donneesCapteurs()
{
    String data = "";

    // mesure de la distance
    distanceValue = distance();
    Serial.print("Distance: ");
    Serial.println(distanceValue);

    // mesure de la température et de l'humidité
    dht_mesure(&temperature, &humidity);

    data = "c" + String(distanceValue) + "," + String(temperature) + "," + String(humidity) + "\n";

    // envoi des données
    Serial.write(data.c_str());
}



/****************************************************/
/*      Fonctions de traitement des capteurs        */
/****************************************************/

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
  while (1) {
    sensors_event_t event;
    dht.temperature().getEvent(&event);
    if (isnan(event.temperature)) {
      // Serial.println(F("Error reading temperature!"));
    }
    else {
      *temperature = event.temperature;
    }
    // Get humidity event and print its value.
    dht.humidity().getEvent(&event);
    if (isnan(event.relative_humidity)) {
      // Serial.println(F("Error reading humidity!"));
    }
    else {
      *humidity = event.relative_humidity;
    }
    delay(delayMS);
  }
}