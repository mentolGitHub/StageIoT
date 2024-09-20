import datetime
from datetime import datetime, timedelta
import json
import math
import requests

api_key="QzeRJulPR1GO90ajkqRLqyAFZR/Ym0mJnXA6D2GHVhI="
url_base = "http://localhost:5000"



# /api/deviceData/<deveui>
eui= "70b3d57ed0068a6f"

start_date= datetime.now()-timedelta(seconds=30)
end_date = datetime.now()

params = {
    "key": api_key,
    "start_date" : start_date,
    "end_date":end_date
}
url = url_base+"/api/deviceData/"+eui
response = requests.get(url, params=params)

res = json.loads(response.content.decode("utf-8"))

if res == None:
    exit()

Spatio_t = {}
Spatio_t[eui]=[]
for i in range(len(res)):
    pos = (res[i]["timestamp"],res[i]['latitude'],res[i]['longitude'], res[i]["angle"],res[i]["azimuth"])
    Spatio_t[eui].append(pos)
print (Spatio_t)


print(datetime.now().timestamp())


params = {
    "key": api_key
}
url = url_base+"/api/objets_proches/"+eui
response = requests.get(url, params=params)
# on recupère les obstacles détectés dans les environs par chaque voisins et on calcule leur position et vitesse si possible.
obstacles = json.loads(response.content.decode("utf-8"))
print(obstacles)
for eui in obstacles:
    if not (eui in Spatio_t):
        url = url_base+"/api/publicDeviceData/"+eui
        response = requests.get(url, params=params)
        res = json.loads(response.content.decode("utf-8"))
        for i in range(len(res)):
            pos = (res[i]["timestamp"],res[i]['latitude'],res[i]['longitude'], res[i]["angle"],res[i]["azimuth"])
            Spatio_t[eui].append(pos)
    for obstacle in obstacles[eui]:
        t=Spatio_t[eui][0][0]
        length_list = len(Spatio_t[eui])
        i = 0
        while t < obstacle["timestamp"] and i < length_list:
            t=Spatio_t[eui][i][0]
            i+=1
        if i != 0:
            v_angle = (math.cos(Spatio_t[eui][i][3]) - math.cos(Spatio_t[eui][i-1][3]), math.sin(Spatio_t[eui][i][3]) - math.sin(Spatio_t[eui][i-1][3]))
            v_azimuth = (math.cos(Spatio_t[eui][i][4]) - math.cos(Spatio_t[eui][i-1][4]), math.sin(Spatio_t[eui][i][4]) - math.sin(Spatio_t[eui][i-1][4]))
            vecteur = (Spatio_t[eui][i][1]- Spatio_t[eui][i-1][1], Spatio_t[eui][i][2]- Spatio_t[eui][i-1][2])
            print("angle : "+v_angle)
            print("azimuth : "+v_azimuth)
            print("vecteur : "+vecteur)
        else:
            pass

        print(t,i)


# /api/neighbourList/<deveui>

# on recupère  les voisins et leur position (angle etc..)

# on retire les doublons en recoupant les données

# on place l'obstacle sur la carte

