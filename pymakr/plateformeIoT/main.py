from machine import UART
from network import LoRa
import pycom
import time
import socket
import ubinascii

print("initialisation ...")

####### Initialisation LED #######
pycom.heartbeat(False) # Desactivation du mode led clignotante
pycom.rgbled(0x000001) # Couleur led bleue pour signaler le démarrage

####### Initialisation UART #######
uart = UART(1, baudrate=9600) # Tx : P3, Rx : P4

####### Initialisation LoRa #######
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868) # Initialise LoRa en mode LORAWAN.

app_eui = ubinascii.unhexlify('70B3D57ED003A31C')
app_key = ubinascii.unhexlify('76F43018D4D2BAD4EB6B433B0C7107D2')
dev_eui = ubinascii.unhexlify('70b3d5499e370b3d')

####### Connexion LoRa #######
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0) # Connexion au réseau LoRaWAN

while not lora.has_joined():        # Attente de connexion au réseau LoRaWAN
    time.sleep(2.5)
    pycom.rgbled(0x010000)          # Couleur led rouge pour signaler la non connexion
    print('Not yet joined...')

pycom.rgbled(0x000100)              # Couleur led verte pour signaler la connexion
print('Joined')

####### Initialisation socket LoRa #######
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5) # fixer le débit de données LoRaWAN

s.setblocking(False) # rendre le socket non bloquant

####### Programme principal #######
while 1 :
    #uart.write('test')
    dataFromLoRa = s.recv(64)                   # Lecture des données LoRa
    if uart.any() > 0:
        dataFromUart = uart.read(uart.any())    # Lecture des données UART
        s.send(dataFromUart)                    # Envoi des données UART par LoRa
        print(dataFromUart)
    time.sleep(2)