acceleratio#include "BluetoothSerial.h"
#include <HardwareSerial.h>
#include <stdio.h>
#include <string.h>

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif


/* Déclaration des objets */

//ports séries
BluetoothSerial SerialBT;
HardwareSerial SerialPort(2); 

//variables de réception
char dataFromBluetooth[] = "";
char dataFromUart[] = "";


/* Déclaration des fonctions */

void traitementReceptionBluetooth();
void traitementDataFromBluetooth();
void traitementReceptionUart();


/* Initialisation */
void setup() 
{
  Serial.begin(9600); //initialisation du port série
  SerialPort.begin(9600, SERIAL_8N1, 16, 17);  //initialisation de l'uart rx : 16 et tx : 17
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
  char timestamp[], latitude[], longitude[], altitude[], luminosite[], vitesseAngulaireX[], vitesseAngulaireY[], vitesseAngulaireZ[], pression[], accelerationX[], accelerationY[], accelerationZ[], angle[], azimut[];
  if (SerialBT.available()) {
    dataFromBluetooth = SerialBT.readString();
    Serial.write(dataFromBluetooth.c_str());
    SerialPort.write(dataFromBluetooth.c_str());
  }
}

void traitementDataFromBluetooth()
{
  char *token = strtok(dataFromBluetooth, ",");
  int i = 0;
  while (token != NULL) {
    while (token != 's' && token != NULL) {
      token = strtok(NULL, ",");
    }
    switch (i) {
      case 0:
        timestamp = token;
        break;
      case 1:
        latitude = token;
        break;
      case 2:
        longitude = token;
        break;
      case 3:
        altitude = token;
        break;
      case 4:
        luminosite = token;
        break;
      case 5:
        vitesseAngulaireX = token;
        break;
      case 6:
        vitesseAngulaireY = token;
        break;
      case 7:
        vitesseAngulaireZ = token;
        break;
      case 8:
        pression = token;
        break;
      case 9:
        accelerationX = token;
        break;
      case 10:
        accelerationY = token;
        break;
      case 11:
        accelerationZ = token;
        break;
      case 12:
        angle = token;
        break;
      case 13:
        azimut = token;
        break;
    }
    token = strtok(NULL, ",");
    i++;
  }
  
}

void traitementReceptionUart()
{
  if (SerialPort.available()) {
    dataFromUart = SerialPort.readString();
    Serial.write(dataFromUart.c_str());
    SerialBT.print(dataFromUart);
  }
}

