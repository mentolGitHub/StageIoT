# API Documentation

This document outlines the usage of various endpoints in the API.

## Base URL

```
http://localhost:5000/api/
```

## Authentication

All requests require an API key, which should be included as a query parameter `key` in each request.

```
apiKey = "WYWe0TXUR1epGePhmm9ZfVFqhiv6n0krj/SD5jAgfZ4="
```

## Endpoints

### 1. Get Device List

Retrieves a list of devices.

- **Endpoint:** `deviceList`
- **Method:** GET
- **Parameters:**
  - `key`: Your API key

**Example Request:**
```python
import requests

url = "http://localhost:5000/api/deviceList"
params = {
    "key": apiKey
}

response = requests.get(url, params=params)
```

**Expected Response:**
```json
[
  {"dev-eui": "device_eui", "name": "device_name"},
  {"dev-eui": "device_eui_2", "name": "device_name_2"}
]
```

### 2. Get Device Data

Retrieves data for a specific device within a given time range.

- **Endpoint:** `deviceData/<deveui>`
- **Method:** GET
- **Parameters:**
  - `key`: Your API key
  - `start_date`: Start date and time for data retrieval (format: "YYYY-MM-DD HH:MM:SS")
  - `end_date`: End date and time for data retrieval (format: "YYYY-MM-DD HH:MM:SS")
  - `dataType`: Type of data to retrieve (use "*" for all data)

**Example Request:**
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

**Expected Response:**
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
    "timestamp": "Mon, 08 Jul 2024 14:39:34 GMT",
    "vitesse_angulaire_X": -0.1831,
    "vitesse_angulaire_Y": 0.02289,
    "vitesse_angulaire_Z": 0.03052
  }
]
```

### 3. Get Neighbour List

Retrieves a list of neighbouring devices for a specific device.

- **Endpoint:** `neighbourList/<deveui>`
- **Method:** GET
- **Parameters:**
  - `key`: Your API key
  - `size`: Size parameter for determining neighbours

**Example Request:**
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

### 4. Register Device

Registers a new device.

- **Endpoint:** `registerDevice`
- **Method:** POST
- **Parameters:**
  - `key`: Your API key
  - `deveui`: Device EUI
  - `name`: Device name
  - `pwd`: Device password

**Example Request:**
```python
import requests

url = "http://localhost:5000/api/registerDevice"
params = {
    "deveui": "70b3d57ed0068a5l",
    "name": "device",
    "pwd": "coucou",
    "key": apiKey
}

response = requests.post(url, params=params)
```

### 5. Delete Device

Deletes a device.

- **Endpoint:** `deleteDevice`
- **Method:** POST
- **Parameters:**
  - `key`: Your API key
  - `deveui`: Device EUI
  - `name`: Device name
  - `pwd`: Device password

**Example Request:**
```python
import requests

url = "http://localhost:5000/api/deleteDevice"
params = {
    "deveui": "70b3d57ed0068a5l",
    "name": "device",
    "pwd": "coucou",
    "key": apiKey
}

response = requests.post(url, params=params)
```

### 6. Get Object

Retrieves information about a specific object.

- **Endpoint:** `getObject/<target_eui>`
- **Method:** GET
- **Parameters:**
  - `key`: Your API key

**Example Request:**
```python
import requests

target_eui = "70b3d57ed0068a6e"
url = f"http://localhost:5000/api/getObject/{target_eui}"
params = {
    "key": apiKey
}

response = requests.get(url, params=params)
```

## Error Handling

For all endpoints, check the response status code. A status code of 200 indicates a successful request. In case of an error, the response will include an error message and status code.

Example error handling:
```python
if response.status_code == 200:
    print(response.json())
else:
    print("Error:", response.status_code)
    print("Message:", response.json().get('message', 'No message provided'))
```