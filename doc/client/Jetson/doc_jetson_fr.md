[retour à l'arborescence de la doc](../README.md)
# Documentation des programmes de la Jetson Orin Nano

## Table des matières 
 
  - Table des matières
  - Introduction
  - Installation
  - Utillité des différents fichiers

## Introduction 

La jetson orin nano sert d'ordinateur central, elle permet donc de choisir a qui envoyer les données, de stocker les données en local et de détécter les objets a partir d'une caméra. 

## Installation 

L'application utilise les dépendances principales suivantes :

- OpenCV (cv2) pour le traitement d'image de la caméra

- DepthAI (dai) pour la profonceur des différents objets

- NumPy pour les calculs

- Serial pour les communications UART (115200 bauds)

- Mysql-connector pour acceder a la base de données locale

- Time 

- Threading afin de paralleliser les différents programmes

- Queue créer des files d'attente pour l'envoi des données

- Datetime afin de connaitre l'heure 


Pour lancer le programme :

1. Allez sur la jetson dans le dossier ```PlateformeCollecteDonnees/src/client/```

2. Lancer main.py (il est possible que l'accès a l'uart soit réservé, dans ce cas, lancez en sudo)


## Fichiers
 
- **Main.py**  : Fichier principal, il va créer les queues et les threads pour lancer les autres programmes. 
 
- **DataCollector.py**  : Ce fichier permet de récupérer les données et les mettre dans la base de donnée locale.
 
- **MiddlewareUnit.py**  : Ce fichier réceptionne les données UART et les redistribue elle transfore aussi les messages en données traitables par les autres fichiers

- **NetworkUnit.py**  : Envoie les données à transmettre en LoRa ou via IP

- **spatial-object-detection.py** : Detecte les objets ainsi que leur emplacement dans l'espace et renvoie le type d'objet ainsi que les coordonnées dans l'espace de l'objet par rapport au centre de la camera (voir la doc dédiée).

Cette documentation fournit un aperçu des composants principaux et des fonctionnalités du programme de détection d'objets spatiaux. Pour plus d'informations détaillées sur chaque fonction ou composant, référez-vous aux commentaires intégrés dans le code source.

[retour à l'arborescence de la doc](../README.md)