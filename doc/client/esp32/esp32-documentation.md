[retour à l'arborescence de la doc](../README.md)
# ESP32 IoT Platform Documentation

## Table of Contents
- [ESP32 IoT Platform Documentation](#esp32-iot-platform-documentation)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Setup](#setup)
  - [Main Components](#main-components)
  - [Communication Interfaces](#communication-interfaces)
  - [Sensor Integration](#sensor-integration)
  - [Data Processing](#data-processing)
  - [Main Loop](#main-loop)
  - [Functions](#functions)
    - [`traitementReceptionBluetooth()`](#traitementreceptionbluetooth)
    - [`traitementReceptionUart()`](#traitementreceptionuart)
    - [`traitementReceptionUartRpi()`](#traitementreceptionuartrpi)
    - [`distance()`](#distance)
    - [`dht_mesure(float* temperature, float* humidity)`](#dht_mesurefloat-temperature-float-humidity)

## Introduction

This ESP32-based IoT platform serves as a versatile data collection and communication hub. It integrates various sensors and communication protocols to gather, process, and transmit environmental and positional data.

## Setup

The application uses the following main dependencies:
- BluetoothSerial
- HardwareSerial
- DHT_Unified
- Adafruit_Sensor

To set up the device:

1. Include necessary libraries
2. Define pin configurations
3. Initialize communication interfaces
4. Set up sensors

## Main Components

- Bluetooth Serial communication
- UART communication
- DHT11 temperature and humidity sensor
- HC-SR04 ultrasonic distance sensor

## Communication Interfaces

- Bluetooth Serial: For wireless communication with other devices
- Hardware Serial: For UART communication with external modules (e.g., LoRa)
- Serial: For debugging, PyCom data transmission and communication with Raspberry Pi/Jetson

## Sensor Integration

- DHT11: Measures temperature and humidity
- HC-SR04: Measures distance
- Smartphone sensors (via bluetooth)

## Data Processing

The device processes various types of data:
- GPS data (latitude, longitude, altitude)
- Environmental data (luminosity, pressure)
- Motion data (angular velocity, acceleration)
- Orientation data (angle, azimuth)
- Sensor data (distance, temperature, humidity)

(not exhaustive, depends on the phone used)

## Main Loop

The main loop consists of three primary functions:
1. `traitementReceptionBluetooth()`: Handles incoming Bluetooth data
2. `traitementReceptionUart()`: Processes UART data from the Pycom module
3. `traitementReceptionUartRpi()`: Manages UART communication with Raspberry Pi / jetson 

## Functions

### `traitementReceptionBluetooth()`
- Processes incoming Bluetooth data
- Parses received data and updates relevant variables
- Constructs and sends LoRa and Bluetooth payloads

### `traitementReceptionUart()`
- Handles UART communication with the Pycom module
- Processes system messages and forwards relevant data

### `traitementReceptionUartRpi()`
- Manages communication with Raspberry Pi / Jetson
- Forwards received data to Bluetooth

### `distance()`
- Measures distance using the HC-SR04 ultrasonic sensor
- Returns distance in centimeters

### `dht_mesure(float* temperature, float* humidity)`
- Continuously measures temperature and humidity using the DHT11 sensor
- Updates provided temperature and humidity pointers
- Runs in a separate thread

This documentation provides an overview of the main components and functionalities of the ESP32 IoT platform. For more detailed information on each function or component, refer to the inline comments in the source code.

[retour à l'arborescence de la doc](../README.md)