# Format des trammes d'envoi de donnnées

## Table des id de trammes


| ID   | Usage       | Description                                                  |
|------|-------------|--------------------------------------------------------------|
| 0    | Système     | Permet au système de remonter des informations sur son état  |
| 1    | Utilisateur | Permet à l'utilisateur déajouter ses propres données         |
| 2-15 | Données     | Permet au systeme de collecte de renvooyer ses données       |


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

| ID | timestamp | Donnée1              | Donnée2               | Donnée3               | Donnée4               |
|----|-----------|----------------------|-----------------------|-----------------------|-----------------------|
| 3  | time      | Longitude            | Latitude              | Altitude              | Luminosité            |
| 4  | time      | Vitesse Angulaire X  | Vitesse Angulaire Y   | Vitesse Angulaire Z   | Préssion              |
| 5  | time      | Accelération X       | Accelération Y        | Accelération Z        | Angle                 |
| 6  | time      | Azimut               | Distance              | Présence              |                  |
