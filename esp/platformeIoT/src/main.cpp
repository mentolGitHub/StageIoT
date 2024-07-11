#include "BluetoothSerial.h"
#include <HardwareSerial.h>
#include <stdio.h>
#include <string.h>
#include <Arduino.h>

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

/* Déclaration des fonctions */

void traitementReceptionBluetooth();
void traitementReceptionUart();
const int triggerPin = 5; // Remplacer par la broche GPIO utilisée pour le Trigger
const int echoPin = 18; // Remplacer par la broche GPIO utilisée pour l'Echo

float distance();
bool is_ip_allowed = false;

/* Initialisation */
void setup() 
{
  Serial.begin(9600); //initialisation du port série
  SerialPort.begin(115200, SERIAL_8N1, 16, 17);  //initialisation de l'uart rx : 16 et tx : 17
  pinMode(triggerPin, OUTPUT);
  pinMode(echoPin, INPUT);
  SerialBT.begin("Plateforme iot"); //initialisation du bluetooth
  Serial.println("The device started, now you can pair it with bluetooth!");
}

/* Main loop */
void loop() 
{
  traitementReceptionBluetooth();
  traitementReceptionUart();
  delay(20);
}


/* Fonctions */

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
          loraPayload = "2" + timestamp + "," + latitude + "," + longitude + "," + altitude + "," + luminosite + "," + vitesseAngulaireX + "," + vitesseAngulaireY + "," + vitesseAngulaireZ + "," + pression + "," + accelerationX + "," + accelerationY + "," + accelerationZ + "," + angle + "," + azimut + "," + distanceValue + "\n";
          SerialPort.print(loraPayload);
          Serial.println("loraPayload : " + loraPayload);
          break;

        case '.':
          distanceValue = distance();
          char formattedDistance[6]; // 5 digits + null terminator
          snprintf(formattedDistance, sizeof(formattedDistance), "%05d", distanceValue);
          btPayload = "30" + String(formattedDistance);
          SerialBT.print(btPayload);
          Serial.println("btPayload : " + btPayload + "\n");
          break;

        default:
          Serial.println("inconnu0 : " + token[0]);
          break;
      }
      
    }
  }
}

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