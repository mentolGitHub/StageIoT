import requests

api_key="f3cwlOMcT52NFYHHJRTWFr1PlsgTuU3lkYeyFyVSzQQ="


params = {
    "key": api_key
}

# /api/deviceData/<deveui>
eui= "70b3d57ed0068a6f"
url = "http://localhost:5000/api/objets_proches/"+eui
response = requests.get(url, params=params)
# on recupère les obstacles détectés dans les environs par chaque voisins et on calcule leur position et vitesse si possible.
print(response.content)


# /api/neighbourList/<deveui>
# /api/publicDeviceData/<deveui>
# on recupère  les voisins et leur position (angle etc..)

# on retire les doublons en recoupant les données

# on place l'obstacle sur la carte

