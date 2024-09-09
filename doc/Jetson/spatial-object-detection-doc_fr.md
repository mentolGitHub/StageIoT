[retour à l'arborescence de la doc](../README.md)
# Documentation de la Détection d'Objets Spatiaux 

## Table des matières 
 
  - Table des matières
  - Introduction
  - Installation
  - Composants principaux
  - Représentation des objets
  - Configuration du pipeline
  - Boucle principale
  - Traitement des données
  - Sortie
  - Fonctions et classes
  - Format des données
  - Informations supplémentaires

## Introduction 

Ce programme implémente la détection d'objets spatiaux en utilisant la bibliothèque DepthAI et OpenCV. Il traite les entrées vidéo provenant d'une configuration de caméra stéréo pour détecter les objets et leurs coordonnées spatiales en 3D.

## Installation 

L'application utilise les dépendances principales suivantes :

- OpenCV (cv2)

- DepthAI (dai)

- NumPy

- Serial

Pour configurer l'appareil :

1. Assurez-vous que le fichier modèle blob DepthAI est disponible

2. Configurez le port série pour la communication UART

3. Configurez le pipeline DepthAI

Pour lancer le programme :
1. Allez sur la jetson dans le dossier ```PlateformeCollecteDonnees/src/client/```

2. Lancer main.py (il est possible que l'accès a l'uart soit réservé, dans ce cas, lancez en sudo)


## Composants principaux 
 
- **Pipeline DepthAI**  : Configure le flux de données pour l'entrée de la caméra et l'inférence du réseau neuronal
 
- **MobileNet-SSD**  : Réseau neuronal pour la détection d'objets (possibilité de choisir d'autres modèles)
 
- **Profondeur stéréo**  : Calcule les informations de profondeur à partir de l'entrée de la caméra stéréo
 
- **Communication UART**  : Envoie les données des objets détectés via le port série (115200 bauds)

## Représentation des objets 
Les objets sont représentés par la classe `ObjetSpatial`, qui inclut :
- Coordonnées 3D (x, y, z)

- Type d'objet

- Méthode pour une représentation sous forme de chaîne formatée

## Configuration du pipeline 

Le pipeline DepthAI est configuré avec les composants suivants :

- Caméra couleur

- Caméras mono (gauche et droite)

- Profondeur stéréo

- Réseau de détection spatiale (MobileNet-SSD)

## Boucle principale 

La boucle principale exécute en continu les étapes suivantes :

1. Récupère des images de la caméra

2. Traite les informations de profondeur

3. Exécute la détection d'objets

4. Formate et envoie les données des objets via UART

## Traitement des données 
 
- **Traitement de la trame de profondeur**  : Normalise et applique une cartographie en couleur des informations de profondeur
 
- **Détection d'objets**  : Applique MobileNet-SSD pour détecter les objets dans la scène
 
- **Calcul spatial**  : Détermine les coordonnées 3D des objets détectés

## Sortie 
 
- **UART**  : Envoie les données formatées des objets (type et coordonnées 3D)
 
- **Affichage visuel (optionnel)**  : Affiche la trame de profondeur cartographiée en couleur et les résultats de détection

## Fonctions et classes 
Classe : `ObjetSpatial`
- Représente un objet détecté avec des coordonnées spatiales
 
- Méthodes : 
  - `__init__(self, x, y, z, type_objet)` : Initialise l'objet
 
  - `__repr__(self)` : Représentation sous forme de chaîne
 
  - `sendingformat(self)` : Chaîne formatée pour la transmission UART

### Fonctions principales du script : 

- Configuration et mise en place du pipeline

- Initialisation de la caméra et du réseau neuronal
 
- Boucle de traitement principale
  - Acquisition des trames

  - Traitement de la profondeur

  - Détection d'objets

  - Formatage et transmission des données

## Format des données
 
  X, Y, Z, Label

  Envoyé via une queue a l'applicaiton main

## Informations supplémentaires

Cette documentation fournit un aperçu des composants principaux et des fonctionnalités du programme de détection d'objets spatiaux. Pour plus d'informations détaillées sur chaque fonction ou composant, référez-vous aux commentaires intégrés dans le code source.

[retour à l'arborescence de la doc](../README.md)