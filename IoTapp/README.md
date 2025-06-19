# 📡 IoT Android App – Geolocation & Orientation via WebSocket

This Android application was developed as part of an **IoT** project. It enables a smartphone connected to a Wi-Fi access point (typically from a microcontroller or embedded platform) to **send real-time geolocation and orientation data** via a **WebSocket connection**.

---

## 📱 Features

- ✅ Automatically connects to the WebSocket server when Wi-Fi is available
- 📍 Sends data every second:
  - **Latitude / Longitude**
  - **Speed** (m/s)
  - **Altitude** (m)
  - **Pitch / Roll / Azimut** (device orientation)
  - **Timestamp** (ISO 8601 UTC)
- 📶 Verifies Wi-Fi connectivity
- 📤 Transmits data using WebSocket in JSON format

---

## Technologies Used
- Android studio
- Java	Main programming language
- Android SDK	Access to sensors, location, permissions
- OkHttp WebSocket	Real-time WebSocket communication
- JSON	Data format for transmission
- Google Play Services	FusedLocationProviderClient for efficient GPS data

## 🧪 Sample JSON Payload

```json
{
  "timestamp": "2025-06-12T14:31:45Z",
  "id": 1,
  "latitude": 48.8566,
  "longitude": 2.3522,
  "altitude": 35.0,
  "speed": 2.4,
  "pitch": -1.2,
  "roll": 4.5,
  "azimut":45
}
  

