from network import LoRa
import pycom
import ubinascii
#
lora = LoRa(mode=LoRa.LORAWAN, region = LoRa.EU868)
mac = lora.mac()
#
print ('devEUI: ', end='')
#
for i in range (0, 8):
 print(hex(mac[i]), end='-')
#
print ()
print ("DevEUI: %s" % (ubinascii.hexlify(lora.mac()).decode('ascii')))