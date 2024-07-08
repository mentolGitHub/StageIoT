import requests
from requests.auth import HTTPBasicAuth

url = "http://147.127.245.67:5000/api/deviceList"

response = requests.get(url, auth=HTTPBasicAuth('a', 'a'))

if response.status_code == 200:
    print(response.json())
else:
    print("Erreur:", response.status_code)