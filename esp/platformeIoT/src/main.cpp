#include "BluetoothSerial.h"
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
String dataFromBluetooth;
String dataFromUart;


/* Déclaration des fonctions */

void traitementReceptionBluetooth();
void traitementReceptionUart();


/* Initialisation */
void setup() 
{
  Serial.begin(9600); //initialisation du port série
  SerialPort.begin(115200, SERIAL_8N1, 16, 17);  //initialisation de l'uart rx : 16 et tx : 17
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
  String timestamp, latitude, longitude, altitude, luminosite, vitesseAngulaireX, vitesseAngulaireY, vitesseAngulaireZ, pression, accelerationX, accelerationY, accelerationZ, angle, azimut;
  if (SerialBT.available()) {
    dataFromBluetooth = SerialBT.readString();
    char buffer[dataFromBluetooth.length() + 1];
    dataFromBluetooth.toCharArray(buffer, sizeof(buffer));
    char *token = strtok(buffer, ",");
    int i = 0;
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
      }
      token = strtok(NULL, ",");
      i++;
    }
    String loraPayload = "2" + timestamp + "," + latitude + "," + longitude + "," + altitude + "," + luminosite + "," + vitesseAngulaireX + "," + vitesseAngulaireY + "," + vitesseAngulaireZ + "," + pression + "," + accelerationX + "," + accelerationY + "," + accelerationZ + "," + angle + "," + azimut + "\n";
    SerialPort.print(loraPayload);
    Serial.println(loraPayload);
  }
}

void traitementReceptionUart()
{
  if (SerialPort.available()) {
    Serial.write(dataFromUart.c_str());
    SerialBT.print(dataFromUart);
  }
}
