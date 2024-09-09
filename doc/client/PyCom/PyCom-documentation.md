[retour à l'arborescence de la doc](../README.md)
# Pycom Program Documentation

## Table of Contents

- [Pycom Program Documentation](#pycom-program-documentation)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Setup](#setup)
  - [Initialization](#initialization)
    - [LED Initialization](#led-initialization)
    - [UART Initialization](#uart-initialization)
    - [LoRa Initialization](#lora-initialization)
  - [LoRa Communication](#lora-communication)
  - [UART Communication](#uart-communication)
  - [LED Control](#led-control)
  - [Data Handling](#data-handling)
    - [Data from UART](#data-from-uart)
    - [Sending Data Buffer](#sending-data-buffer)
    - [Timing](#timing)
    - [Utility Function](#utility-function)

## Introduction

This Pycom program manages communication via LoRa and UART for an IoT device. It initializes the necessary components, sends and receives data, and controls the LED indicators to signal different states of the device.

## Setup

The program uses the following main dependencies:

* `machine`
* `network`
* `pycom`
* `time`
* `socket`
* `ubinascii`
* `struct`

To run the program, ensure your Pycom device is set up with the required libraries and the network configurations are correct.

## Initialization

### LED Initialization

The program initializes the LED to signal the start-up process.

```python
pycom.heartbeat(False)  # Disable the default blinking LED mode
pycom.rgbled(0x000001)  # Set LED color to blue to signal startup
```

### UART Initialization

The UART is initialized for serial communication with external components.

```python
uart = UART(1, baudrate=115200)  # Tx: P3, Rx: P4
```

### LoRa Initialization

The LoRa module is initialized for communication in LoRaWAN mode.

```python
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)  # Initialize LoRa in LORAWAN mode

app_eui = '7532159875321598'
app_key = '11CBA1678ECF54273F5834C41D82E57F'
dev_eui = '70B3D57ED0068A6E'

app_eui_unhex = ubinascii.unhexlify(app_eui)
app_key_unhex = ubinascii.unhexlify(app_key)
dev_eui_unhex = ubinascii.unhexlify(dev_eui)
```

## LoRa Communication

This section configures and manages LoRa communication. It sets up the necessary identifiers and establishes the connection to the LoRa network.

## UART Communication

The program initializes UART for serial communication, reading and writing data via UART.

## LED Control

LED control is used to signal different states of the device, such as initialization and data transmission.

- red : initialization problem / no gateway available
- orange : not connected to LoRaWAN
- green : connected


## Data Handling

### Data from UART

Data received from UART is stored in a variable.

```python
dataFromUart = ""
```

### Sending Data Buffer

A buffer is prepared for sending data.

```python
idTramme = 2
sendBuffer = struct.pack('i', idTramme)
```

### Timing

Timing is managed to control the frequency of operations.

```python
oldTimer = time.time()
```

### Utility Function

A utility function is provided to check if a value is a float.

```python
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
```

This documentation provides an overview of the main components and functionalities of the Pycom program. For more detailed information on each function or section, refer to the inline comments in the source code.

[retour à l'arborescence de la doc](../README.md)