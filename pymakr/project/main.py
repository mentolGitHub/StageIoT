from network import LoRa
import socket
import time
import ubinascii
import pycom
from machine import Pin
import utime
import machine 


## renvoi la distance en cm (mesure par ultrasons)
def distance():
    #initialisation des pins
    trig = Pin('P23', mode = Pin.OUT)
    echo = Pin('P22', mode = Pin.IN)
    
    # envoie d'une impulsion de 10us
    trig.value(0)
    time.sleep(1/1000000)
    trig.value(1)
    time.sleep(11/1000000)
    trig.value(0)
    
    # mesure du temps de propagation
    while echo() == 0:
        pass
    start = utime.ticks_us()

    while echo() == 1:
        pass
    finish = utime.ticks_us()
    
    duree = finish-start
    
    # calcul de la distance
    distance = duree * 340 / 2 / 10000 # 340 : vitesse du son en m/s / 2 : aller-retour / 10000 : pour passer de µs en s
    
    return distance
    
    
def niveau_liquide():
    adc = machine.ADC()
    apin = adc.channel(pin='P16')
    niveau = apin.voltage()
    return niveau

import struct

def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])


def rx_callback():
    s.setblocking(False)
    data = s.recv(64)
    s.setblocking(True)
    if data :
        print(data)


pycom.heartbeat(False)

# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# create an OTAA authentication parameters, change them to the provided credentials
app_eui = ubinascii.unhexlify('70B3D57ED0038811')
app_key = ubinascii.unhexlify('583FE2F370E3F43BCFE06291DCD155A1')
#uncomment to use LoRaWAN application provided dev_eui
dev_eui = ubinascii.unhexlify('70b3d5499e370b3d')

# join a network using OTAA (Over the Air Activation)
#uncomment below to use LoRaWAN application provided dev_eui
#lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    pycom.rgbled(0x101000)
    time.sleep(0.3)
    pycom.rgbled(0x000000)
    time.sleep(0.3)
    

print('Joined')
pycom.rgbled(0x001000)
# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)


# send some data
while 1 :
    s.setblocking(True)
    data_dist = 0.2   #distance()
    print(data_dist)
    
    byte = struct.pack("f", data_dist)

    #print("bytes : {}".format(struct.unpack("f", byte)))
    s.send(byte)

    
# def send_float(float):
#     data= struct.pack("f", float)
#     send(data)

# def send_str(string):
#     data =bytes(string,"utf-8")
    
#     data = base64.b64encode(data)
#     data = data.decode()
#     send(data)