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

String loraPayload = "";

/* Déclaration des fonctions */

void traitementReceptionBluetooth();
void traitementReceptionUart();


/* Initialisation */
void setup() 
{
  Serial.begin(115200); //initialisation du port série
  SerialPort.begin(115200, SERIAL_8N1, 16, 17);  //initialisation de l'uart rx : 16 et tx : 17
  SerialBT.begin("Plateforme iot"); //initialisation du bluetooth
  Serial.println("The device started, now you can pair it with bluetooth!");
}

/* Main loop */
void loop() 
{
  traitementReceptionBluetooth();
  //traitementReceptionUart();
}


/* Fonctions */

void traitementReceptionBluetooth()
{
  String timestamp, latitude, longitude, altitude, luminosite, vitesseAngulaireX, vitesseAngulaireY, vitesseAngulaireZ, pression, accelerationX, accelerationY, accelerationZ, angle, azimut;
  if (SerialBT.available()) {
    String dataFromBluetooth = SerialBT.readStringUntil('\n');
    dataFromBluetooth.trim(); // Supprimer les espaces et les caractères de nouvelle ligne
    if (dataFromBluetooth.length() > 0) {
      //Serial.println("Données reçues : " + dataFromBluetooth);
      // Traitez vos données ici
    

      char buffer[dataFromBluetooth.length() + 1];
      dataFromBluetooth.toCharArray(buffer, sizeof(buffer));
      char *token = strtok(buffer, ",");
      int i = 1;
      //detection du type de données recues
      if (token != NULL)
      {
        // detection d'objets
        if (strcmp(token,"o") == 0)
        {
          loraPayload = dataFromBluetooth;
          SerialPort.println(loraPayload);
          Serial.println(loraPayload);
        }
        //données de capteurs
        else if (strcmp(token,"s") == 0)
        {
          String loraPayload = "";
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
          loraPayload = "2" + timestamp + "," + latitude + "," + longitude + "," + altitude + "," + luminosite + "," + vitesseAngulaireX + "," + vitesseAngulaireY + "," + vitesseAngulaireZ + "," + pression + "," + accelerationX + "," + accelerationY + "," + accelerationZ + "," + angle + "," + azimut + "\n";
          SerialPort.print(loraPayload);
          Serial.println(loraPayload);
        }
      }
    }
  }
}

void traitementReceptionUart()
{
  if (SerialPort.available()) {
    dataFromUart = SerialPort.readString();
    //verifier le premier caractere
    switch (dataFromUart[0])
    {
      case '0':
        switch (dataFromUart[1])
        {
          case '1': //envoi du dev eui
            SerialBT.print(dataFromUart.substring(2));
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
