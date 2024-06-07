from network import LoRa
import socket
import time
import ubinascii
import pycom

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
s.setblocking(True)

# send some data
while 1 :

    table = "1,2,3"
    s.send(bytes(table))

    # make the socket non-blocking
    # (because if there's no data received it will block forever...)
    s.setblocking(False)

    # get any data received (if any...)
    data = s.recv(64)
    if data :
        print(data)
    time.sleep(1)
    
