[retour à l'arborescence de la doc](../README.md)
# Documentation de la Plateforme IoT ESP32

## Table des matières

- [Documentation de la Plateforme IoT ESP32](#documentation-de-la-plateforme-iot-esp32)
  - [Table des matières](#table-des-matières)
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Composants principaux](#composants-principaux)
  - [Interfaces de communication](#interfaces-de-communication)
  - [Intégration des capteurs](#intégration-des-capteurs)
  - [Traitement des données](#traitement-des-données)
  - [Boucle principale](#boucle-principale)
  - [Fonctions](#fonctions)
    - [`traitementReceptionBluetooth()`](#traitementreceptionbluetooth)
    - [`traitementReceptionUartLoPy()`](#traitementreceptionuartlopy)
    - [`traitementReceptionUartJetson()`](#traitementreceptionuartjetson)
    - [`distance()`](#distance)
    - [`dht_mesure(float* temperature, float* humidity)`](#dht_mesurefloat-temperature-float-humidity)

## Introduction

L'ESP32 sert de hub polyvalent pour la collecte de données et la communication. Il permet à la fois de récolter les données des différents capteurs, de se connecter a un smartphone en bluetooth pour en extraire les données et de faire la liaison entre la Jetson et l'émetteur LoRa.

## Installation

L'application utilise les dépendances suivantes :

* BluetoothSerial pour la communication bluetooth avec le smartphone
* HardwareSerial pour la communication en uart avec les différentes cartes
* DHT_Unified pour le capteur DHT11 (humidité/température)
* Adafruit_Sensor pour les autres capteurs(distance)

Pour configurer l'appareil :

1. Inclure les bibliothèques nécessaires
2. Définir les configurations des broches
3. Initialiser les interfaces de communication
4. Configurer les capteurs

Pour flasher le programme sur l'esp32

1. Installer l'extension platformio sur vscode
2. Ouvrir le dossier dans vscode ```StageIoT\esp\platformeIoT```
3. Aller dans l'onglet PlatformIO : PROJECT TASKS
4. Cliquer sur upload (et sur le bouton "en" de l'esp si nécésssaire)

Attention : le port série de l'esp ne doit pas être en cours d'utilisation lors du téléversement 

Il est aussi possible d'utiliser arduino ide pour téléverser sur l'esp (bien penser a télécharger les lib)

## Composants principaux

* Communication série via Bluetooth
* Communication UART
* Capteur de température et d'humidité DHT11 (optionnel)
* Capteur de distance ultrasonique HC-SR04 (optionnel)

## Interfaces de communication

* Bluetooth Serial : pour la communication sans fil avec d'autres appareils
* Hardware Serial : pour la communication UART avec des modules externes (par exemple, LoRa), touts les communications UART se font en 115200 bauds
* Serial : pour le débogage et la communication avec un Raspberry Pi/Jetson orin nano (115200 bauds)

## Intégration des capteurs

* DHT11 : mesure la température et l'humidité (optionnel)
* HC-SR04 : mesure la distance (optionnel)
* Capteurs du smartphone (via Bluetooth)

## Traitement des données

L'appareil traite différents types de données :

* Données GPS (latitude, longitude, altitude)
* Données environnementales (luminosité, pression)
* Données de mouvement (vitesse angulaire, accélération)
* Données d'orientation (angle, azimut)
* Données des capteurs (distance, température, humidité)

(La liste n'est pas exhaustive, cela dépend du téléphone utilisé)

## Boucle principale

La boucle principale se compose de trois fonctions principales :

1. `traitementReceptionBluetooth()` : gère les données entrantes via Bluetooth
2. `traitementReceptionUart()` : traite les données UART provenant du module Pycom
3. `traitementReceptionUartJetson()` : gère la communication UART avec une Raspberry Pi ou une Jetson

## Fonctions

### `traitementReceptionBluetooth()`

* Traite les données entrantes via Bluetooth
* Analyse les données reçues et met à jour les variables pertinentes
* Construit et envoie les charges utiles pour LoRa et Bluetooth

### `traitementReceptionUartLoPy()`

* Gère la communication UART avec le module Pycom
* Transmet les données à la jetson ainsi qu'au téléphone

### `traitementReceptionUartJetson()`

* Gère la communication avec le Raspberry Pi ou le Jetson
* Transmet les données reçues vers le Bluetooth

### `distance()`

* Mesure la distance à l'aide du capteur ultrasonique HC-SR04
* Renvoie la distance en centimètres

### `dht_mesure(float* temperature, float* humidity)`

* Mesure en continu la température et l'humidité à l'aide du capteur DHT11
* Met à jour les pointeurs de température et d'humidité fournis
* Fonctionne dans un thread séparé

Cette documentation fournit un aperçu des principaux composants et fonctionnalités de la plateforme IoT ESP32. Pour des informations plus détaillées sur chaque fonction ou composant, veuillez consulter les commentaires dans le code source.

[retour à l'arborescence de la doc](../README.md)