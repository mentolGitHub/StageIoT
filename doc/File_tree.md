# Arborescence des dossiers 

## Sommaire

- [Arborescence des dossiers simple](#arborescence-des-dossiers-simple)
- [Arborescence avec description des dossiers](#arborescence-avec-description-des-dossiers)
- [Arborescence avec description des dossiers et fichiers](#arborescence-avec-description-des-dossiers-et-fichiers)

## Arborescence des dossiers simple

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
 ┃ ┃ ┣ 📂.vscode
 ┃ ┃ ┃ ┣ 📜extensions.json
 ┃ ┃ ┃ ┗ 📜settings.json
 ┃ ┃ ┣ 📂include
 ┃ ┃ ┃ ┗ 📜README
 ┃ ┃ ┣ 📂lib
 ┃ ┃ ┃ ┗ 📜README
 ┃ ┃ ┣ 📂src
 ┃ ┃ ┃ ┗ 📜main.cpp
 ┃ ┃ ┣ 📂test
 ┃ ┃ ┃ ┗ 📜README
 ┃ ┃ ┣ 📜.gitignore
 ┃ ┃ ┗ 📜platformio.ini
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
 ┃ ┃ ┃ ┣ 📂web
 ┃ ┃ ┃ ┃ ┣ 📂static
 ┃ ┃ ┃ ┃ ┃ ┣ 📂img
 ┃ ┃ ┃ ┃ ┃ ┃ ┗ 📜iotcar.png
 ┃ ┃ ┃ ┃ ┃ ┣ 📂styles
 ┃ ┃ ┃ ┃ ┃ ┃ ┣ 📜deviceList.css
 ┃ ┃ ┃ ┃ ┃ ┃ ┗ 📜styles.css
 ┃ ┃ ┃ ┃ ┃ ┣ 📜favicon.ico
 ┃ ┃ ┃ ┃ ┃ ┗ 📜index.js
 ┃ ┃ ┃ ┃ ┣ 📂templates
 ┃ ┃ ┃ ┃ ┃ ┣ 📜deviceList.html
 ┃ ┃ ┃ ┃ ┃ ┣ 📜download.html
 ┃ ┃ ┃ ┃ ┃ ┣ 📜edit_device.html
 ┃ ┃ ┃ ┃ ┃ ┣ 📜index.html
 ┃ ┃ ┃ ┃ ┃ ┣ 📜login.html
 ┃ ┃ ┃ ┃ ┃ ┣ 📜map.html
 ┃ ┃ ┃ ┃ ┃ ┣ 📜objects.html
 ┃ ┃ ┃ ┃ ┃ ┣ 📜objets_proches.html
 ┃ ┃ ┃ ┃ ┃ ┣ 📜profile.html
 ┃ ┃ ┃ ┃ ┃ ┣ 📜register.html
 ┃ ┃ ┃ ┃ ┃ ┣ 📜register_device.html
 ┃ ┃ ┃ ┃ ┃ ┗ 📜visualize.html
 ┃ ┃ ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┃ ┃ ┗ 📜IP.cpython-312.pyc
 ┃ ┃ ┃ ┃ ┗ 📜IP.py
 ┃ ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┃ ┣ 📜Interface.cpython-312.pyc
 ┃ ┃ ┃ ┃ ┣ 📜MQTT.cpython-312.pyc
 ┃ ┃ ┃ ┃ ┗ 📜utils.cpython-312.pyc
 ┃ ┃ ┃ ┣ 📜config.conf
 ┃ ┃ ┃ ┣ 📜Interface.py
 ┃ ┃ ┃ ┣ 📜main.py
 ┃ ┃ ┃ ┣ 📜MQTT.py
 ┃ ┃ ┃ ┣ 📜stageiot.sql
 ┃ ┃ ┃ ┗ 📜utils.py
 ┃ ┗ 📜Readme.md
 ┣ 📂pymakr
 ┃ ┗ 📂plateformeIoT
 ┃ ┃ ┣ 📜boot.py
 ┃ ┃ ┣ 📜main.py
 ┃ ┃ ┗ 📜pymakr.conf
 ┣ 📜.gitignore
 ┣ 📜arborescence-fichiers-projet.md
 ┣ 📜lauch.sh
 ┣ 📜README.md
 ┗ 📜requirements.txt
 ```

## Arborescence avec description des dossiers

```
📦StageIoT
 ┣ 📂doc ----------------------------  Documentation du projet
 ┃ ┣ 📂api --------------------------  Documentation de l'api
 ┃ ┃ ┣ 📜api_doc.md
 ┃ ┃ ┣ 📜documentation-api-fr.md
 ┃ ┃ ┣ 📜example_api.py 
 ┃ ┃ ┗ 📜README.md
 ┃ ┣ 📂client -----------------------  Documentation du client
 ┃ ┃ ┣ 📂esp32 ----------------------  Documentation du code de l'esp32
 ┃ ┃ ┃ ┣ 📜esp32-documentation.md
 ┃ ┃ ┃ ┣ 📜esp32-documentation_fr.md
 ┃ ┃ ┃ ┗ 📜README.md
 ┃ ┃ ┣ 📂Jetson ---------------------  Documentation du code de la Jetson Orin Nano
 ┃ ┃ ┃ ┣ 📜BDD_client.drawio.png
 ┃ ┃ ┃ ┣ 📜BDD_client.drawio.svg
 ┃ ┃ ┃ ┣ 📜doc_jetson_fr.md
 ┃ ┃ ┃ ┣ 📜README.md
 ┃ ┃ ┃ ┣ 📜spatial-object-detection-doc.md
 ┃ ┃ ┃ ┗ 📜spatial-object-detection-doc_fr.md
 ┃ ┃ ┣ 📂PyCom ---------------------  Documentation du code de la LoPy4
 ┃ ┃ ┃ ┣ 📜documentation-pycom-fr.md
 ┃ ┃ ┃ ┣ 📜PyCom-documentation.md
 ┃ ┃ ┃ ┗ 📜README.md
 ┃ ┃ ┣ 📜cablage.drawio.png
 ┃ ┃ ┣ 📜cablage.drawio.svg
 ┃ ┃ ┗ 📜README.md
 ┃ ┣ 📂server ----------------------  Documentation du code du serveur
 ┃ ┃ ┣ 📜DB.png
 ┃ ┃ ┣ 📜DB.svg
 ┃ ┃ ┣ 📜flask-app-documentation.md
 ┃ ┃ ┗ 📜README.md
 ┃ ┣ 📜payloadFormat.md
 ┃ ┗ 📜README.md
 ┣ 📂esp ---------------------------  Code de l'esp32
 ┃ ┗ 📂platformeIoT ----------------  Dossier du projet PlatformIO
 ┃ ┃ ┣ 📂include -------------------  Dossier pour les includes (vide)
 ┃ ┃ ┃ ┗ 📜README
 ┃ ┃ ┣ 📂lib -----------------------  Dossier pour les libs (vide)
 ┃ ┃ ┃ ┗ 📜README
 ┃ ┃ ┣ 📂src -----------------------  Fichiers sources
 ┃ ┃ ┃ ┗ 📜main.cpp
 ┃ ┃ ┣ 📂test ----------------------  Fichiers des codes a tester (vide)
 ┃ ┃ ┃ ┗ 📜README
 ┃ ┃ ┣ 📜.gitignore
 ┃ ┃ ┗ 📜platformio.ini
 ┣ 📂PlateformeCollecteDonnees 
 ┃ ┣ 📂examples --------------------  Fichiers d'exemples
 ┃ ┃ ┣ 📂api -----------------------  Exemples d'utilisation de l'api
 ┃ ┃ ┃ ┣ 📜api_doc.md
 ┃ ┃ ┃ ┣ 📜example_api.py
 ┃ ┃ ┃ ┗ 📜Readme.md
 ┃ ┃ ┗ 📜share_neighbour_data.py
 ┃ ┣ 📂img -------------------------  Schémas 
 ┃ ┃ ┣ 📜DiagClient.svg
 ┃ ┃ ┣ 📜Diagramme Client (Jetson).png
 ┃ ┃ ┣ 📜Diagramme sans nom.drawio
 ┃ ┃ ┗ 📜schema_bdd.png
 ┃ ┣ 📂src -------------------------  Fichiers sources
 ┃ ┃ ┣ 📂client --------------------  Sources du client
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
 ┃ ┃ ┗ 📂serveur -------------------  Sources du serveur
 ┃ ┃ ┃ ┣ 📂web ---------------------  Serveur web (Flask)
 ┃ ┃ ┃ ┃ ┣ 📂static ----------------  Dossier des static 
 ┃ ┃ ┃ ┃ ┃ ┣ 📂img -----------------  Images
 ┃ ┃ ┃ ┃ ┃ ┃ ┗ 📜iotcar.png
 ┃ ┃ ┃ ┃ ┃ ┣ 📂styles --------------  Fichiers CSS
 ┃ ┃ ┃ ┃ ┃ ┃ ┣ 📜deviceList.css
 ┃ ┃ ┃ ┃ ┃ ┃ ┗ 📜styles.css
 ┃ ┃ ┃ ┃ ┃ ┣ 📜favicon.ico
 ┃ ┃ ┃ ┃ ┃ ┗ 📜index.js
 ┃ ┃ ┃ ┃ ┣ 📂templates -------------  Pages web
 ┃ ┃ ┃ ┃ ┃ ┣ 📜deviceList.html
 ┃ ┃ ┃ ┃ ┃ ┣ 📜download.html
 ┃ ┃ ┃ ┃ ┃ ┣ 📜edit_device.html
 ┃ ┃ ┃ ┃ ┃ ┣ 📜index.html
 ┃ ┃ ┃ ┃ ┃ ┣ 📜login.html
 ┃ ┃ ┃ ┃ ┃ ┣ 📜map.html
 ┃ ┃ ┃ ┃ ┃ ┣ 📜objects.html
 ┃ ┃ ┃ ┃ ┃ ┣ 📜objets_proches.html
 ┃ ┃ ┃ ┃ ┃ ┣ 📜profile.html
 ┃ ┃ ┃ ┃ ┃ ┣ 📜register.html
 ┃ ┃ ┃ ┃ ┃ ┣ 📜register_device.html
 ┃ ┃ ┃ ┃ ┃ ┗ 📜visualize.html
 ┃ ┃ ┃ ┃ ┣ 📂__pycache__ -----------  Cache de python (sert à rien)
 ┃ ┃ ┃ ┃ ┃ ┗ 📜IP.cpython-312.pyc
 ┃ ┃ ┃ ┃ ┗ 📜IP.py
 ┃ ┃ ┃ ┣ 📂__pycache__ -------------  Cache de python (sert à rien)
 ┃ ┃ ┃ ┃ ┣ 📜Interface.cpython-312.pyc
 ┃ ┃ ┃ ┃ ┣ 📜MQTT.cpython-312.pyc
 ┃ ┃ ┃ ┃ ┗ 📜utils.cpython-312.pyc
 ┃ ┃ ┃ ┣ 📜config.conf
 ┃ ┃ ┃ ┣ 📜Interface.py
 ┃ ┃ ┃ ┣ 📜main.py
 ┃ ┃ ┃ ┣ 📜MQTT.py
 ┃ ┃ ┃ ┣ 📜stageiot.sql
 ┃ ┃ ┃ ┗ 📜utils.py
 ┃ ┗ 📜Readme.md
 ┣ 📂pymakr ------------------------  Codes pour la PyCom
 ┃ ┗ 📂plateformeIoT ---------------  Dossier du projet de la PyCom (LoPy4)
 ┃ ┃ ┣ 📜boot.py
 ┃ ┃ ┣ 📜main.py
 ┃ ┃ ┗ 📜pymakr.conf
 ┣ 📜.gitignore
 ┣ 📜arborescence-fichiers-projet.md
 ┣ 📜lauch.sh
 ┣ 📜README.md
 ┗ 📜requirements.txt
 ```

 ## Arborescence avec description des dossiers et fichiers

```
📦StageIoT
 ┣ 📂doc ============================  Documentation du projet
 ┃ ┣ 📂api ==========================  Documentation de l'api
 ┃ ┃ ┣ 📜api_doc.md -----------------  Documentation de l'api en anglais
 ┃ ┃ ┣ 📜documentation-api-fr.md ----  Documenatation de l'api en francais
 ┃ ┃ ┣ 📜example_api.py -------------  Exemple d'utilisation de l'api
 ┃ ┃ ┗ 📜README.md ------------------  Sommaire de la doc de l'api
 ┃ ┣ 📂client =======================  Documentation du client
 ┃ ┃ ┣ 📂esp32 ======================  Documentation du code de l'esp32
 ┃ ┃ ┃ ┣ 📜esp32-documentation.md ---  Documentation du code de l'esp en anglais
 ┃ ┃ ┃ ┣ 📜esp32-documentation_fr.md   Documentation du code de l'esp en francais
 ┃ ┃ ┃ ┗ 📜README.md ----------------  Sommaire de la doc de l'esp32
 ┃ ┃ ┣ 📂Jetson =====================  Documentation du code de la Jetson Orin Nano
 ┃ ┃ ┃ ┣ 📜BDD_client.drawio.png ----  Schéma de la base de donnée de la jetson
 ┃ ┃ ┃ ┣ 📜BDD_client.drawio.svg ----  Schéma de la base de donnée de la jetson
 ┃ ┃ ┃ ┣ 📜doc_jetson_fr.md ---------  Documentation du code de la Jetson
 ┃ ┃ ┃ ┣ 📜README.md ----------------  Sommaire de la doc de la Jetson Orin Nano
 ┃ ┃ ┃ ┣ 📜spatial-object-detection-doc.md     Documentation du code de la detection d'objet en anglais
 ┃ ┃ ┃ ┗ 📜spatial-object-detection-doc_fr.md  Documentation du code de la detection d'objet en francais
 ┃ ┃ ┣ 📂PyCom =====================  Documentation du code de la LoPy4
 ┃ ┃ ┃ ┣ 📜documentation-pycom-fr.md  Documentation du code de la LoPy4 en francais
 ┃ ┃ ┃ ┣ 📜PyCom-documentation.md --  Documentation du code de LoPy4 en anglais
 ┃ ┃ ┃ ┗ 📜README.md ---------------  Sommaire de la doc de PyCom
 ┃ ┃ ┣ 📜cablage.drawio.png --------  Schéma de cablage
 ┃ ┃ ┣ 📜cablage.drawio.svg --------  Schéma de cablage
 ┃ ┃ ┗ 📜README.md -----------------  Sommaire de la doc de la documentation du client
 ┃ ┣ 📂server ======================  Documentation du code du serveur
 ┃ ┃ ┣ 📜DB.png --------------------  Schéma de la base de donnée du serveur
 ┃ ┃ ┣ 📜DB.svg --------------------  Schéma de la base de donnée du serveur
 ┃ ┃ ┣ 📜flask-app-documentation.md   Documentation du code du serveur Flask
 ┃ ┃ ┗ 📜README.md -----------------  Sommaire de la doc de la documentation du serveur
 ┃ ┣ 📜payloadFormat.md ------------  Format des trammes de données échangées
 ┃ ┗ 📜README.md -----------------  Sommaire de la doc de la documentation globale
 ┣ 📂esp ===========================  Code de l'esp32
 ┃ ┗ 📂platformeIoT ================  Dossier du projet PlatformIO
 ┃ ┃ ┣ 📂include ===================  Dossier pour les includes (vide)
 ┃ ┃ ┃ ┗ 📜README ------------------  vide
 ┃ ┃ ┣ 📂lib =======================  Dossier pour les libs (vide)
 ┃ ┃ ┃ ┗ 📜README ------------------  vide
 ┃ ┃ ┣ 📂src =======================  Fichiers sources
 ┃ ┃ ┃ ┗ 📜main.cpp ----------------  code de l'esp32
 ┃ ┃ ┣ 📂test ======================  Fichiers des codes a tester (vide)
 ┃ ┃ ┃ ┗ 📜README ------------------  vide
 ┃ ┃ ┣ 📜.gitignore ----------------  pour ne pas envoyer les fichiers de compilation sur le git
 ┃ ┃ ┗ 📜platformio.ini ------------  Configuration de platformIO
 ┣ 📂PlateformeCollecteDonnees 
 ┃ ┣ 📂examples ====================  Fichiers d'exemples
 ┃ ┃ ┣ 📂api =======================  Exemples d'utilisation de l'api
 ┃ ┃ ┃ ┣ 📜api_doc.md --------------  Doc de l'api
 ┃ ┃ ┃ ┣ 📜example_api.py ----------  Exemple d'utilisation de l'api
 ┃ ┃ ┃ ┗ 📜Readme.md
 ┃ ┃ ┗ 📜share_neighbour_data.py ---  Exemple 
 ┃ ┣ 📂img =========================  Schémas 
 ┃ ┃ ┣ 📜DiagClient.svg
 ┃ ┃ ┣ 📜Diagramme Client (Jetson).png
 ┃ ┃ ┣ 📜Diagramme sans nom.drawio
 ┃ ┃ ┗ 📜schema_bdd.png
 ┃ ┣ 📂src =========================  Fichiers sources
 ┃ ┃ ┣ 📂client ====================  Sources du client
 ┃ ┃ ┃ ┣ 📜config.conf -------------  Fichier de configuration du client
 ┃ ┃ ┃ ┣ 📜dataCollector.py --------  Programme du thread de mise en base de donnée
 ┃ ┃ ┃ ┣ 📜main.py -----------------  Fichier principal
 ┃ ┃ ┃ ┣ 📜MiddlewareUnit.py -------  Thread de collecte de l'uart
 ┃ ┃ ┃ ┣ 📜mobilenet-ssd_openvino_2021.4_6shave.blob  Ia de detection d'objet
 ┃ ┃ ┃ ┣ 📜NetworkUnit.py ----------  Thread de transmission LoRa/IP
 ┃ ┃ ┃ ┣ 📜Readme.md 
 ┃ ┃ ┃ ┣ 📜spatial_object_detection.py  Thread de détéction d'objet dans l'espace
 ┃ ┃ ┃ ┣ 📜stageiot.sql ------------  Fichier de configuration de la base de donnée SQL du client
 ┃ ┃ ┃ ┗ 📜test.py
 ┃ ┃ ┗ 📂serveur ===================  Sources du serveur
 ┃ ┃ ┃ ┣ 📂web =====================  Serveur web (Flask)
 ┃ ┃ ┃ ┃ ┣ 📂static ================  Dossier des static 
 ┃ ┃ ┃ ┃ ┃ ┣ 📂img =================  Images
 ┃ ┃ ┃ ┃ ┃ ┃ ┗ 📜iotcar.png --------  La super image de la page d'accueil mal détourée
 ┃ ┃ ┃ ┃ ┃ ┣ 📂styles ==============  Fichiers CSS
 ┃ ┃ ┃ ┃ ┃ ┃ ┣ 📜deviceList.css ----  CSS de la liste d'appareils
 ┃ ┃ ┃ ┃ ┃ ┃ ┗ 📜styles.css --------  CSS global du site
 ┃ ┃ ┃ ┃ ┃ ┣ 📜favicon.ico ---------  Icone de la barre de navigation
 ┃ ┃ ┃ ┃ ┃ ┗ 📜index.js ------------  JS du site (dark mode, ...)
 ┃ ┃ ┃ ┃ ┣ 📂templates =============  Pages web
 ┃ ┃ ┃ ┃ ┃ ┣ 📜deviceList.html -----  Page de la liste des appareils
 ┃ ┃ ┃ ┃ ┃ ┣ 📜download.html -------  Page de téléchargement des données
 ┃ ┃ ┃ ┃ ┃ ┣ 📜edit_device.html ----  Page d'édition d'un appareil
 ┃ ┃ ┃ ┃ ┃ ┣ 📜index.html ----------  Page de base
 ┃ ┃ ┃ ┃ ┃ ┣ 📜login.html ----------  Page de connexion
 ┃ ┃ ┃ ┃ ┃ ┣ 📜map.html ------------  Carte avec les appareils affichés
 ┃ ┃ ┃ ┃ ┃ ┣ 📜objects.html --------  Liste des objets détéctés
 ┃ ┃ ┃ ┃ ┃ ┣ 📜objets_proches.html -  Liste des objets proches
 ┃ ┃ ┃ ┃ ┃ ┣ 📜profile.html --------  Page de profil utilisateur
 ┃ ┃ ┃ ┃ ┃ ┣ 📜register.html -------  Page de création d'un nouvel utilisateur
 ┃ ┃ ┃ ┃ ┃ ┣ 📜register_device.html   Page d'enregistrement d'une nouvelle plateforme
 ┃ ┃ ┃ ┃ ┃ ┗ 📜visualize.html ------  Page de visualisation des graphs super stylée
 ┃ ┃ ┃ ┃ ┣ 📂__pycache__ ===========  Cache de python (sert à rien)
 ┃ ┃ ┃ ┃ ┃ ┗ 📜IP.cpython-312.pyc
 ┃ ┃ ┃ ┃ ┗ 📜IP.py -----------------  Serveur Flask
 ┃ ┃ ┃ ┣ 📂__pycache__ =============  Cache de python (sert à rien)
 ┃ ┃ ┃ ┃ ┣ 📜Interface.cpython-312.pyc
 ┃ ┃ ┃ ┃ ┣ 📜MQTT.cpython-312.pyc
 ┃ ┃ ┃ ┃ ┗ 📜utils.cpython-312.pyc
 ┃ ┃ ┃ ┣ 📜config.conf -------------  Configuration du serveur 
 ┃ ┃ ┃ ┣ 📜Interface.py ------------  
 ┃ ┃ ┃ ┣ 📜main.py -----------------  Lancement du serveur
 ┃ ┃ ┃ ┣ 📜MQTT.py
 ┃ ┃ ┃ ┣ 📜stageiot.sql ------------  Base de données du serveur
 ┃ ┃ ┃ ┗ 📜utils.py
 ┃ ┗ 📜Readme.md
 ┣ 📂pymakr ========================  Codes pour la PyCom
 ┃ ┗ 📂plateformeIoT ===============  Dossier du projet de la PyCom (LoPy4)
 ┃ ┃ ┣ 📜boot.py -------------------  Lancement au démarrage de la PyCom (vide)
 ┃ ┃ ┣ 📜main.py -------------------  Main
 ┃ ┃ ┗ 📜pymakr.conf  --------------  Config de PyMakr (l'extension pour flasher la PyCom)
 ┣ 📜.gitignore --------------------  Pour pas push les trucs inutiles sur le git
 ┣ 📜arborescence-fichiers-projet.md
 ┣ 📜lauch.sh ----------------------  Script d'installation de pleins de trucs super
 ┣ 📜README.md
 ┗ 📜requirements.txt --------------  Libs python nécéssaires (peut etre pas complet)
 ```