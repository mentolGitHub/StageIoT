# Documentation de l'Application Flask

## Table des Matières
- [Documentation de l'Application Flask](#documentation-de-lapplication-flask)
  - [Table des Matières](#table-des-matières)
  - [Introduction](#introduction)
  - [Configuration](#configuration)
  - [Routes](#routes)
    - [Routes Principales](#routes-principales)
    - [Routes d'Authentification](#routes-dauthentification)
    - [Routes de Gestion des Appareils](#routes-de-gestion-des-appareils)
    - [Routes de Données](#routes-de-données)
  - [Authentification](#authentification)
  - [Opérations sur la Base de Données](#opérations-sur-la-base-de-données)
  - [Points d'Accès API](#points-daccès-api)
  - [Fonctions Utilitaires](#fonctions-utilitaires)

## Introduction

Cette application Flask fournit une interface web et une API pour gérer des appareils IoT et leurs données. Elle inclut l'authentification des utilisateurs, l'enregistrement des appareils, la visualisation des données et des points d'accès API pour récupérer les données des appareils.

## Configuration

L'application utilise les dépendances principales suivantes :
- Flask
- Flask-WTF
- Flask-HTTPAuth
- Flask-RESTful
- Flask-CORS
- MySQL Connector

Pour exécuter l'application :

```python
from queue import Queue
config = {...}  # Ajoutez votre configuration ici
IPnode(Queue(), config)
```

## Routes

### Routes Principales

- `/` : Page d'accueil
- `/objects` : Page des objets
- `/visualize` : Page de visualisation des données
- `/map` : Page de vue cartographique
- `/profile` : Page de profil utilisateur

### Routes d'Authentification

- `/login` : Connexion utilisateur
- `/register` : Inscription utilisateur
- `/logout` : Déconnexion utilisateur

### Routes de Gestion des Appareils

- `/register_device` : Enregistrer un nouvel appareil
- `/deviceList` : Liste des appareils de l'utilisateur
- `/edit_device/<deveui>` : Modifier les détails d'un appareil
- `/delete_device/<deveui>` : Supprimer un appareil

### Routes de Données

- `/post_data` : Recevoir et traiter les données des appareils
- `/get_data` : Récupérer les données des appareils
- `/get_objects` : Obtenir les données des objets
- `/get_euiList` : Obtenir la liste des EUI des appareils
- `/downloadall` : Télécharger toutes les données en CSV
- `/download` : Télécharger les données sélectionnées en CSV
- `/objets_proches/<deveui>` : Obtenir les objets proches d'un appareil

## Authentification

L'application utilise une authentification basée sur les sessions pour les routes web et une authentification par jeton pour les points d'accès API. Les fonctions incluent :

- `verify_token(t)` : Vérifier le jeton d'authentification
- `check_user_token()` : Vérifier le jeton utilisateur et retourner le nom d'utilisateur
- `get_user_from_api_key(api_key)` : Obtenir le nom d'utilisateur à partir de la clé API

## Opérations sur la Base de Données

Les opérations sur la base de données sont effectuées en utilisant MySQL. Les fonctions clés incluent :

- `check_device_DB(deveui, password=None)` : Vérifier l'appareil dans la base de données
- `add_device_DB(deveui, name, hashed_password)` : Ajouter un appareil à la base de données
- `add_device_user_DB(deveui, username, superowner=0)` : Associer un appareil à un utilisateur
- `delete_device(deveui, username)` : Supprimer un appareil de la base de données

## Points d'Accès API

- `/api/deviceList` : Obtenir la liste des appareils de l'utilisateur
- `/api/deviceData/<deveui>` : Obtenir les données d'un appareil spécifique
- `/api/publicDeviceData/<deveui>` : Obtenir les données publiques d'un appareil
- `/api/registerDevice` : Enregistrer un nouvel appareil
- `/api/deleteDevice` : Supprimer un appareil
- `/api/neighbourList/<deveui>` : Obtenir la liste des appareils voisins
- `/api/getObject/<deveui>` : Obtenir les données d'objet pour un appareil

Pour plus d'informations, consultez la documentation de l'API

## Fonctions Utilitaires

- `hash_password(password)` : Hacher le mot de passe en utilisant bcrypt
- `check_password(hashed_password, user_password)` : Vérifier le mot de passe
- `calculate_object_coordinates(emetteur_lat, emetteur_long, object_dist, object_x)` : Calculer les coordonnées de l'objet
- `add_data_to_cache(data)` : Ajouter des données au cache en mémoire

Cette documentation fournit un aperçu des principaux composants et fonctionnalités de l'application Flask. Pour des informations plus détaillées sur chaque fonction ou route, référez-vous aux commentaires dans le code source.
