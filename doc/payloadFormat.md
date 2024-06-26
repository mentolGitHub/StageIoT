# Format des trammes d'envoi de donnnées LoRa

## Table des id de trammes


| ID   | Usage       | Description                                                  |
|------|-------------|--------------------------------------------------------------|
| 0    | Système     | Permet au système de remonter des informations sur son état  |
| 1    | Utilisateur | Permet à l'utilisateur d'ajouter ses propres données         |
| 2-15 | Données     | Permet au systeme de collecte d'envoyer ses données       |


## Trammes systèmes
ce format permet au système de faire remonter des messages au serveur via de courts messages
| ID | timestamp | Donnée 1        |
|----|-----------|-----------------|
| 0  | time      | Message système |

## Trammes Utilisateur

ce format permet à l'utilisateur de définir sa propre tramme

| ID | SubID | timestamp | Données |
|----|-------|-----------|---------|
| 1  | 0-15  | time      | Message |

## Trammes de données

| ID | timestamp | Donnée1              | Donnée2               | Donnée3               | Donnée4        | Donnée5       | taille totale |
|----|-----------|----------------------|-----------------------|-----------------------|----------------|---------------|---------------|
| 2  | time      | Longitude            | Latitude              | Altitude              | Angle          |               |               |
| 3  | time      | Vitesse Angulaire X  | Vitesse Angulaire Y   | Vitesse Angulaire Z   | Pression       |               |               |
| 4  | time      | Accelération X       | Accelération Y        | Accelération Z        | Température    |               |               |
| 5  | time      | Azimut               | Distance              | Présence              | Luminosité     | Humidité      |               |
| 6  | time      | Charge moteur        |                       |                       |                |               |               |


# Format des trammes d'envoi de donnnées Bluetooth

s, timestamp, latitude, longitude, altitude, luminosité, vitesse angulaire X, vitesse angulaire Y, vitesse angulaire Z, pression, accélérationX, accélérationY, accélérationZ, angle, azimut