# Format des trammes d'envoi de donnnées LoRa

## Table des id de trammes


| ID   | Usage       | Description                                                  |
|------|-------------|--------------------------------------------------------------|
| 0    | Système     | Permet au système de remonter des informations sur son état  |
| 1    | Utilisateur | Permet à l'utilisateur d'ajouter ses propres données         |
| 2-15 | Données     | Permet au systeme de collecte d'envoyer ses données          |


## Trammes systèmes
ce format permet au système de faire remonter des messages au serveur via de courts messages
| ID | timestamp | Donnée 1        |
|----|-----------|-----------------|
| 0  | oui       | Message système |

| ID | SubId | timestamp | Donnée 1        |
|----|-------|-----------|-----------------|
| 0  |   1   | non       | DevEui          |
| 0  |   2   | non       | activation 4g   |

## Trammes Utilisateur

ce format permet à l'utilisateur de définir sa propre tramme

| ID | SubID | timestamp | Données |
|----|-------|-----------|---------|
| 1  | 0-15  | oui       | Message |

## Trammes de données

| ID  | subId | timestamp | Donnée               | Donnée                | Donnée                | Donnée         | Donnée        |  Donnée              |
|-----|-------|-----------|----------------------|-----------------------|-----------------------|----------------|---------------|----------------------|
|  2  |  non  | oui       | Latitude             | Longitude             | Altitude              | Angle          | luminosite    | Vitesse Angulaire X  |
|     |       |           | Vitesse Angulaire Y  | Vitesse Angulaire Z   | Pression              | Accelération X | Accelération Y| Accelération Z       | 
|     |       |           | Angle                | Azimut                |                       |                |               |                      |
|  3  |   0   | non       | Distance             |                       |                       |                |               |                      |



# Format des trammes d'envoi de donnnées Bluetooth

s, timestamp, latitude, longitude, altitude, luminosité, vitesse angulaire X, vitesse angulaire Y, vitesse angulaire Z, pression, accélérationX, accélérationY, accélérationZ, angle, azimut
o, objet1, objet2, ...

020\n desactivation 4g
021\n activation 4g
30 distance\n envoi de la distance