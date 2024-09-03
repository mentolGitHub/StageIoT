# Plateforme IoT pour véhicules

## Description du projet
Ce projet vise à développer une plateforme IoT pour collecter et transmettre des données de véhicules en utilisant un réseau de capteurs et en les transmettant via le réseau mobile ou LoRa.

## Fonctionnalités principales
- Collecte de données de véhicules via des capteurs
- Transmission des données via réseau mobile ou LoRa
- Visualisation des données depuis un site web
- Recuperation des données via une API

## Materiel utilisé

### Jetson Orin Nano
    La jetson Orin Nano ser l'ordinateur central a notre projet, elle va gerer le traitement des données mais aussi servire a faire toutes les opérations de traitement de l'image.

### ESP32
    La catre ESP32 permet de servir de carte d'aquisition a la foir pour récupérer les données des capteurs mais aussi pour se connecter facilement en bluetooth à un appareil mobile.

### LoPy4
    La carte LoPy4 sert émetteur recepteur Lora, elle pourrait être remplacé par un limple émetteur/recepteur

### Camera OAK-D
    La caméra OAK-D permet de facilement faire de la reconnaissance d'image (avec la jetson, il serait possible d'uiliser une camera basique grace aux connecteurs csi)

## Technologies utilisées
### Transmission de données : 
- Internet (IP) (2G, 3G, 4G, 5G)
- LoRaWan via TTN

## Installation
```bash
    ./launch.sh
```
puis creer une base de données sql et l'initialiser avec le fichier stageiot.sql
```sql
    use stageiot.sql
```
## Configuration
dossier config.conf pour la partie serveur

## Utilisation
Brancher une esp et téléverser son programme 
Brancher une lopy4 et téléverser son programme (en entrant bien les information de connexion au reseau LoRa)
Installer l'application mobile
lancer l'application mobile et se connecter a la plateforme en bluetooth
