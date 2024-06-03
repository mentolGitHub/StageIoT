from network import LoRa
import pycom
import ubinascii
import time

pycom.heartbeat(False)

i=0
while True:
    #colors in hexadecimal (0xRRGGBB)
    pycom.rgbled(0xFF0000)  # Red
    time.sleep(1)
    pycom.rgbled(0x00FF00)  # Green
    time.sleep(1)
    pycom.rgbled(0x0000FF)  # Blue
    time.sleep(1)
    print(i)
    i += 1

# #
# lora = LoRa(mode=LoRa.LORAWAN, region = LoRa.EU868)
# mac = lora.mac()
# #
# print ('devEUI: ', end='')
# #
# for i in range (0, 8):
#  print(hex(mac[i]), end='-')
# #
# print ()
# print ("DevEUI: %s" % (ubinascii.hexlify(lora.mac()).decode('ascii')))