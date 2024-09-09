# Documentation de l'API

Ce document décrit l'utilisation des différents points de terminaison de l'API.

## URL de Base

```
http://localhost:5000/api/
```

## Authentification

Toutes les requêtes nécessitent une clé API, qui doit être incluse comme paramètre de requête `key` dans chaque demande.

```
apiKey = "WYWe0TXUR1epGePhmm9ZfVFqhiv6n0krj/SD5jAgfZ4="
```

## Points de Terminaison

### 1. Obtenir la Liste des Appareils

Récupère une liste d'appareils.

- **Point de terminaison :** `deviceList`
- **Méthode :** GET
- **Paramètres :**
  - `key`: Votre clé API

**Exemple de Requête :**
```python
import requests

url = "http://localhost:5000/api/deviceList"
params = {
    "key": apiKey
}

response = requests.get(url, params=params)
```

**Réponse Attendue :**
```json
[
  {"dev-eui": "eui_appareil", "name": "nom_appareil"},
  {"dev-eui": "eui_appareil_2", "name": "nom_appareil_2"}
]
```

### 2. Obtenir les Données d'un Appareil

Récupère les données d'un appareil spécifique dans une plage de temps donnée.

- **Point de terminaison :** `deviceData/<deveui>`
- **Méthode :** GET
- **Paramètres :**
  - `key`: Votre clé API
  - `start_date`: Date et heure de début pour la récupération des données (format : "AAAA-MM-JJ HH:MM:SS")
  - `end_date`: Date et heure de fin pour la récupération des données (format : "AAAA-MM-JJ HH:MM:SS")
  - `dataType`: Type de données à récupérer (utilisez "*" pour toutes les données)

**Exemple de Requête :**
```python
import requests

deveui = "70b3d57ed0068a6f"
url = f"http://localhost:5000/api/deviceData/{deveui}"
params = {
    "start_date": "2024-07-10 10:12:10",
    "end_date": "2024-07-10 10:12:20",
    "dataType": "*",
    "key": apiKey
}

response = requests.get(url, params=params)
```

**Réponse Attendue :**
```json
[
  {
    "acceleration_X": 0.75135,
    "acceleration_Y": -1.02174,
    "acceleration_Z": 9.7352,
    "altitude": 198.7,
    "angle": -36.4559,
    "azimuth": 320.835,
    "distance_recul": 16.0,
    "humidity": null,
    "latitude": 43.6025,
    "longitude": 1.45469,
    "luminosity": 752.598,
    "presence": null,
    "pression": null,
    "source": "70b3d57ed0068a6f",
    "temperature": null,
    "timestamp": "Lun, 08 Jul 2024 14:39:34 GMT",
    "vitesse_angulaire_X": -0.1831,
    "vitesse_angulaire_Y": 0.02289,
    "vitesse_angulaire_Z": 0.03052
  }
]
```

### 3. Obtenir la Liste des Voisins

Récupère une liste des appareils voisins pour un appareil spécifique.

- **Point de terminaison :** `neighbourList/<deveui>`
- **Méthode :** GET
- **Paramètres :**
  - `key`: Votre clé API
  - `size`: Paramètre de taille pour déterminer les voisins

**Exemple de Requête :**
```python
import requests

deveui = "70b3d57ed0068a6f"
url = f"http://localhost:5000/api/neighbourList/{deveui}"
params = {
    "size": 0.002,
    "key": apiKey
}

response = requests.get(url, params=params)
```

### 4. Enregistrer un Appareil

Enregistre un nouvel appareil.

- **Point de terminaison :** `registerDevice`
- **Méthode :** POST
- **Paramètres :**
  - `key`: Votre clé API
  - `deveui`: EUI de l'appareil
  - `name`: Nom de l'appareil
  - `pwd`: Mot de passe de l'appareil

**Exemple de Requête :**
```python
import requests

url = "http://localhost:5000/api/registerDevice"
params = {
    "deveui": "70b3d57ed0068a5l",
    "name": "appareil",
    "pwd": "motdepasse",
    "key": apiKey
}

response = requests.post(url, params=params)
```

### 5. Supprimer un Appareil

Supprime un appareil.

- **Point de terminaison :** `deleteDevice`
- **Méthode :** POST
- **Paramètres :**
  - `key`: Votre clé API
  - `deveui`: EUI de l'appareil
  - `name`: Nom de l'appareil
  - `pwd`: Mot de passe de l'appareil

**Exemple de Requête :**
```python
import requests

url = "http://localhost:5000/api/deleteDevice"
params = {
    "deveui": "70b3d57ed0068a5l",
    "name": "appareil",
    "pwd": "motdepasse",
    "key": apiKey
}

response = requests.post(url, params=params)
```

### 6. Obtenir un Objet

Récupère des informations sur un objet spécifique.

- **Point de terminaison :** `getObject/<target_eui>`
- **Méthode :** GET
- **Paramètres :**
  - `key`: Votre clé API

**Exemple de Requête :**
```python
import requests

target_eui = "70b3d57ed0068a6e"
url = f"http://localhost:5000/api/getObject/{target_eui}"
params = {
    "key": apiKey
}

response = requests.get(url, params=params)
```

## Gestion des Erreurs

Pour tous les points de terminaison, vérifiez le code de statut de la réponse. Un code de statut 200 indique une requête réussie. En cas d'erreur, la réponse inclura un message d'erreur et un code de statut.

Exemple de gestion des erreurs :
```python
if response.status_code == 200:
    print(response.json())
else:
    print("Erreur:", response.status_code)
    print("Message:", response.json().get('message', 'Aucun message fourni'))
```
