import requests
from datetime import datetime, timedelta

apiField = "neighbourList"
deveui = "70b3d57ed0068a6f"
apiKey = "xzHF9qEQT+W8t+KaDIgSt+jQxB8RwUrDuji27JSjRmw="
url = "http://localhost:5000/api/"

params = {
    "size": 0.0001,
    "key": apiKey
}

response = requests.get(url+apiField+"/"+deveui, params=params)

if response.status_code == 200:
    pass
if response.status_code == 401:
    print("Error: "+response.json()["error"])
else:
    print("Error:", response.status_code)


params = {
    "start_date": datetime.now()- timedelta(seconds=15),
    "end_date": datetime.now(),
    "dataType": "*",
    "key": apiKey
}
deviceData = []
for i in response.json():
    if i[0] != deveui:
        print (i[0])
        deviceData.append(requests.get(url+"deviceData/"+i[0], params=params).json())

print (deviceData)