[retour à l'arborescence de la doc](../README.md)
# Documentation du Programme Pycom

## Table des Matières

- [Documentation du Programme Pycom](#documentation-du-programme-pycom)
  - [Table des Matières](#table-des-matières)
  - [Introduction](#introduction)
  - [Configuration](#configuration)
  - [Initialisation](#initialisation)
    - [Initialisation de la LED](#initialisation-de-la-led)
    - [Initialisation de l'UART](#initialisation-de-luart)
    - [Initialisation de LoRa](#initialisation-de-lora)
  - [Communication LoRa](#communication-lora)
  - [Communication UART](#communication-uart)
  - [Contrôle de la LED](#contrôle-de-la-led)
  - [Gestion des Données](#gestion-des-données)
    - [Données de l'UART](#données-de-luart)
    - [Envoi du Tampon de Données](#envoi-du-tampon-de-données)
    - [Temporisation](#temporisation)
    - [Fonction Utilitaire](#fonction-utilitaire)

## Introduction

Ce programme Pycom gère la communication via LoRa et UART pour un appareil IoT. Il initialise les composants nécessaires, envoie et reçoit des données, et contrôle les indicateurs LED pour signaler différents états de l'appareil.

## Configuration

Le programme utilise les principales dépendances suivantes :

* `machine`
* `network`
* `pycom`
* `time`
* `socket`
* `ubinascii`
* `struct`

Pour exécuter le programme, assurez-vous que votre appareil Pycom est configuré avec les bibliothèques requises et que les configurations réseau sont correctes.

## Initialisation

### Initialisation de la LED

Le programme initialise la LED pour signaler le processus de démarrage.

```python
pycom.heartbeat(False)  # Désactive le mode de clignotement LED par défaut
pycom.rgbled(0x000001)  # Définit la couleur de la LED sur bleu pour signaler le démarrage
```

### Initialisation de l'UART

L'UART est initialisé pour la communication série avec des composants externes.

```python
uart = UART(1, baudrate=115200)  # Tx: P3, Rx: P4
```

### Initialisation de LoRa

Le module LoRa est initialisé pour la communication en mode LoRaWAN.

```python
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)  # Initialise LoRa en mode LORAWAN

app_eui = '7532159875321598'
app_key = '11CBA1678ECF54273F5834C41D82E57F'
dev_eui = '70B3D57ED0068A6E'

app_eui_unhex = ubinascii.unhexlify(app_eui)
app_key_unhex = ubinascii.unhexlify(app_key)
dev_eui_unhex = ubinascii.unhexlify(dev_eui)
```

## Communication LoRa

Cette section configure et gère la communication LoRa. Elle met en place les identifiants nécessaires et établit la connexion au réseau LoRa.

## Communication UART

Le programme initialise l'UART pour la communication série, lisant et écrivant des données via UART.

## Contrôle de la LED

Le contrôle de la LED est utilisé pour signaler différents états de l'appareil, tels que l'initialisation et la transmission de données.

- rouge : problème d'initialisation / pas de passerelle disponible
- orange : non connecté à LoRaWAN
- vert : connecté

## Gestion des Données

### Données de l'UART

Les données reçues de l'UART sont stockées dans une variable.

```python
dataFromUart = ""
```

### Envoi du Tampon de Données

Un tampon est préparé pour l'envoi des données.

```python
idTramme = 2
sendBuffer = struct.pack('i', idTramme)
```

### Temporisation

La temporisation est gérée pour contrôler la fréquence des opérations.

```python
oldTimer = time.time()
```

### Fonction Utilitaire

Une fonction utilitaire est fournie pour vérifier si une valeur est un nombre flottant.

```python
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
```

Cette documentation fournit un aperçu des principaux composants et fonctionnalités du programme Pycom. Pour des informations plus détaillées sur chaque fonction ou section, référez-vous aux commentaires intégrés dans le code source.

[retour à l'arborescence de la doc](../README.md)