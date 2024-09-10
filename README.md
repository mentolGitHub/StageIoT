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

## Arborescence de fichiers

### Dossiers

```
📦StageIoT
 ┣ 📂doc
 ┃ ┣ 📂api
 ┃ ┣ 📂client
 ┃ ┃ ┣ 📂esp32
 ┃ ┃ ┣ 📂Jetson
 ┃ ┃ ┗ 📂PyCom
 ┃ ┗ 📂server
 ┣ 📂esp
 ┃ ┗ 📂platformeIoT
 ┃   ┣ 📂.vscode
 ┃   ┣ 📂include
 ┃   ┣ 📂lib
 ┃   ┣ 📂src
 ┃   ┗ 📂test
 ┣ 📂PlateformeCollecteDonnees
 ┃ ┣ 📂examples
 ┃ ┃ ┗ 📂api
 ┃ ┣ 📂img
 ┃ ┗ 📂src
 ┃   ┣ 📂client
 ┃   ┗ 📂serveur
 ┃     ┣ 📂web
 ┃     ┃ ┣ 📂static
 ┃     ┃ ┃ ┣ 📂img
 ┃     ┃ ┃ ┗ 📂styles
 ┃     ┃ ┣ 📂templates
 ┃     ┃ ┗ 📂__pycache__
 ┃     ┗ 📂__pycache__
 ┗ 📂pymakr
   ┗ 📂plateformeIoT

 ```

### Dossiers + fichiers

```
📦StageIoT
 ┣ 📂doc
 ┃ ┣ 📂api
 ┃ ┃ ┣ 📜api_doc.md
 ┃ ┃ ┣ 📜documentation-api-fr.md
 ┃ ┃ ┣ 📜example_api.py
 ┃ ┃ ┗ 📜README.md
 ┃ ┣ 📂client
 ┃ ┃ ┣ 📂esp32
 ┃ ┃ ┃ ┣ 📜esp32-documentation.md
 ┃ ┃ ┃ ┣ 📜esp32-documentation_fr.md
 ┃ ┃ ┃ ┗ 📜README.md
 ┃ ┃ ┣ 📂Jetson
 ┃ ┃ ┃ ┣ 📜BDD_client.drawio.png
 ┃ ┃ ┃ ┣ 📜BDD_client.drawio.svg
 ┃ ┃ ┃ ┣ 📜doc_jetson_fr.md
 ┃ ┃ ┃ ┣ 📜README.md
 ┃ ┃ ┃ ┣ 📜spatial-object-detection-doc.md
 ┃ ┃ ┃ ┗ 📜spatial-object-detection-doc_fr.md
 ┃ ┃ ┣ 📂PyCom
 ┃ ┃ ┃ ┣ 📜documentation-pycom-fr.md
 ┃ ┃ ┃ ┣ 📜PyCom-documentation.md
 ┃ ┃ ┃ ┗ 📜README.md
 ┃ ┃ ┣ 📜cablage.drawio.png
 ┃ ┃ ┣ 📜cablage.drawio.svg
 ┃ ┃ ┗ 📜README.md
 ┃ ┣ 📂server
 ┃ ┃ ┣ 📜DB.png
 ┃ ┃ ┣ 📜DB.svg
 ┃ ┃ ┣ 📜flask-app-documentation.md
 ┃ ┃ ┗ 📜README.md
 ┃ ┣ 📜File_tree.md
 ┃ ┣ 📜payloadFormat.md
 ┃ ┗ 📜README.md
 ┣ 📂esp
 ┃ ┗ 📂platformeIoT
 ┃   ┣ 📂.vscode
 ┃   ┃ ┣ 📜extensions.json
 ┃   ┃ ┗ 📜settings.json
 ┃   ┃ ┣ 📂include
 ┃   ┃ ┗ 📜README
 ┃   ┣ 📂lib
 ┃   ┃ ┗ 📜README
 ┃   ┣ 📂src
 ┃   ┃ ┗ 📜main.cpp
 ┃   ┣ 📂test
 ┃   ┃ ┗ 📜README
 ┃   ┣ 📜.gitignore
 ┃   ┗ 📜platformio.ini
 ┣ 📂PlateformeCollecteDonnees
 ┃ ┣ 📂examples
 ┃ ┃ ┣ 📂api
 ┃ ┃ ┃ ┣ 📜api_doc.md
 ┃ ┃ ┃ ┣ 📜example_api.py
 ┃ ┃ ┃ ┗ 📜Readme.md
 ┃ ┃ ┗ 📜share_neighbour_data.py
 ┃ ┣ 📂img
 ┃ ┃ ┣ 📜DiagClient.svg
 ┃ ┃ ┣ 📜Diagramme Client (Jetson).png
 ┃ ┃ ┣ 📜Diagramme sans nom.drawio
 ┃ ┃ ┗ 📜schema_bdd.png
 ┃ ┣ 📂src
 ┃ ┃ ┣ 📂client
 ┃ ┃ ┃ ┣ 📜config.conf
 ┃ ┃ ┃ ┣ 📜dataCollector.py
 ┃ ┃ ┃ ┣ 📜main.py
 ┃ ┃ ┃ ┣ 📜MiddlewareUnit.py
 ┃ ┃ ┃ ┣ 📜mobilenet-ssd_openvino_2021.4_6shave.blob
 ┃ ┃ ┃ ┣ 📜NetworkUnit.py
 ┃ ┃ ┃ ┣ 📜Readme.md
 ┃ ┃ ┃ ┣ 📜spatial_object_detection.py
 ┃ ┃ ┃ ┣ 📜stageiot.sql
 ┃ ┃ ┃ ┗ 📜test.py
 ┃ ┃ ┗ 📂serveur
 ┃ ┃   ┃ ┣ 📂web
 ┃ ┃   ┃ ┣ 📂static
 ┃ ┃   ┃ ┃ ┣ 📂img
 ┃ ┃   ┃ ┃ ┃ ┗ 📜iotcar.png
 ┃ ┃   ┃ ┃ ┣ 📂styles
 ┃ ┃   ┃ ┃ ┃ ┣ 📜deviceList.css
 ┃ ┃   ┃ ┃ ┃ ┗ 📜styles.css
 ┃ ┃   ┃ ┃ ┣ 📜favicon.ico
 ┃ ┃   ┃ ┃ ┗ 📜index.js
 ┃ ┃   ┃ ┣ 📂templates
 ┃ ┃   ┃ ┃ ┣ 📜deviceList.html
 ┃ ┃   ┃ ┃ ┣ 📜download.html
 ┃ ┃   ┃ ┃ ┣ 📜edit_device.html
 ┃ ┃   ┃ ┃ ┣ 📜index.html
 ┃ ┃   ┃ ┃ ┣ 📜login.html
 ┃ ┃   ┃ ┃ ┣ 📜map.html
 ┃ ┃   ┃ ┃ ┣ 📜objects.html
 ┃ ┃   ┃ ┃ ┣ 📜objets_proches.html
 ┃ ┃   ┃ ┃ ┣ 📜profile.html
 ┃ ┃   ┃ ┃ ┣ 📜register.html
 ┃ ┃   ┃ ┃ ┣ 📜register_device.html
 ┃ ┃   ┃ ┃ ┗ 📜visualize.html
 ┃ ┃   ┃ ┣ 📂__pycache__
 ┃ ┃   ┃ ┃ ┗ 📜IP.cpython-312.pyc
 ┃ ┃   ┃ ┗ 📜IP.py
 ┃ ┃   ┣ 📂__pycache__
 ┃ ┃   ┃ ┣ 📜Interface.cpython-312.pyc
 ┃ ┃   ┃ ┣ 📜MQTT.cpython-312.pyc
 ┃ ┃   ┃ ┗ 📜utils.cpython-312.pyc
 ┃ ┃   ┣ 📜config.conf
 ┃ ┃   ┣ 📜Interface.py
 ┃ ┃   ┣ 📜main.py
 ┃ ┃   ┣ 📜MQTT.py
 ┃ ┃   ┣ 📜stageiot.sql
 ┃ ┃   ┗ 📜utils.py
 ┃ ┗ 📜Readme.md
 ┣ 📂pymakr
 ┃ ┗ 📂plateformeIoT
 ┃   ┣ 📜boot.py
 ┃   ┣ 📜main.py
 ┃   ┗ 📜pymakr.conf
 ┣ 📜.gitignore
 ┣ 📜arborescence-fichiers-projet.md
 ┣ 📜lauch.sh
 ┣ 📜README.md
 ┗ 📜requirements.txt
 ```


