from network import LoRa
import socket
import time
import ubinascii
import pycom

pycom.heartbeat(False)

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, coding_rate=LoRa.CODING_4_5)


# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)

s.setblocking(True)
events = lora.events()
# send some data
while 1 :
    while not (events & LoRa.RX_PACKET_EVENT):
        events = lora.events()
        print("envoi")
        pycom.rgbled(0x100000)
        time.sleep(0.5)
        s.send("pong")
    pycom.rgbled(0x001000)
    data = s.recv(64)
    
