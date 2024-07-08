import requests
from requests.auth import HTTPBasicAuth

# This is an example of how to get the device list from the API.

# server URL
url = "http://localhost:5000/api/"


#######################################
#       Device list example           #
#######################################

apiField = "deviceList"

response = requests.get(url+apiField)

if response.status_code == 200:
    print(response.json())
else:
    print("Erreur:", response.status_code)

# Expected output:
#[{'dev-eui': 'device_eui', 'name': 'device_name'}, {'dev-eui': 'device_eui_2', 'name': 'device_name_2'}]



#######################################
#       Device list example           #
#######################################

apiField = "deviceData"
deveui = "70b3d57ed0068a6f"

response = requests.get(url+apiField+"/"+deveui)

if response.status_code == 200:
    print(response.json())
else:
    print("Erreur:", response.status_code)

# Expected output: 
# [{'acceleration_X': 0.75135, 'acceleration_Y': -1.02174, 'acceleration_Z': 9.7352, 'altitude': 198.7, 'angle': -36.4559, 'azimuth': 320.835, 'distance_recul': 16.0, 'humidity': None, 'latitude': 43.6025, 'longitude': 1.45469, 'luminosity': 752.598, 'presence': None, 'pression': None, 'source': '70b3d57ed0068a6f', 'temperature': None, 'timestamp': 'Mon, 08 Jul 2024 14:39:34 GMT', 'vitesse_angulaire_X': -0.1831, 'vitesse_angulaire_Y': 0.02289, 'vitesse_angulaire_Z': 0.03052}]
