from queue import Queue
from machine import UART
from network import LoRa
import pycom
import time
import socket
import ubinascii
import struct
import _thread

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


dataFromUart = ""
idTramme = 2
sendBuffer = struct.pack('i', idTramme)
oldTimer = time.time()

print("initialisation")

####### Initialisation LED #######
pycom.heartbeat(False) # Desactivation du mode led clignotante
pycom.rgbled(0x000001) # Couleur led bleue pour signaler le démarrage

####### Initialisation UART #######
uart = UART(1, baudrate=115200) # Tx : P3, Rx : P4

####### Initialisation LoRa #######
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868) # Initialise LoRa en mode LORAWAN.

app_eui = '7532159875321598'
app_key = '11CBA1678ECF54273F5834C41D82E57F'
dev_eui = '70B3D57ED0068A6F'

app_eui_unhex = ubinascii.unhexlify(app_eui)
app_key_unhex = ubinascii.unhexlify(app_key)
dev_eui_unhex = ubinascii.unhexlify(dev_eui)

####### Connexion LoRa #######
lora.join(activation=LoRa.OTAA, auth=(dev_eui_unhex, app_eui_unhex, app_key_unhex), timeout=0) # Connexion au réseau LoRaWAN



while not lora.has_joined():        # Attente de connexion au réseau LoRaWAN
    time.sleep(2.5)
    pycom.rgbled(0x010000)          # Couleur led rouge pour signaler la non connexion
    uart.write("01"+dev_eui.lower()+"\n") 
    print("envoi eui")
    print('Not yet joined...')

pycom.rgbled(0x000100)              # Couleur led verte pour signaler la connexion
print('Joined')

####### Initialisation socket LoRa #######
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5) # fixer le débit de données LoRaWAN

s.setblocking(True)

def send(Q_out : Queue):
    while True:
        if not Q_out.empty():
            data = Q_out.get()
            # print("data sent")
            print(data)
            s.send(data)
        if not Q_outObj.empty():
            data = Q_outObj.get()
            print("data sent")
            print(data)
            s.send(data)

Q_out = Queue(2)
Q_outObj = Queue(4)
_thread.start_new_thread(send, (Q_out,))
dataFromUart = uart.read(uart.any()).decode('utf-8').split('\n')
####### Programme principal #######
while 1 :
    #uart.write('test')
    #dataFromLoRa = s.recv(64)                   # Lecture des données LoRa
    dataFromUart = ""
    
    # if uart.any() == 0:
    #     while uart.any() == 0:
    #         pass
    # while uart.any() != 0 and char !='\n':
    #     char = uart.read().decode('utf-8')
    #     dataFromUart+= char
    #     print(char)
    while uart.any() != 0:
        time.sleep(0.1)
        dataFromUart = uart.read(uart.any()).decode('utf-8').split('\n')
        # print(dataFromUart)
        for msg in dataFromUart:
            if len(msg)>2:
                a = msg[0]
                print("msg : "+msg)
                if a == '2':
                    if Q_out.full():
                        Q_out.get()
                    Q_out.put(msg)
                elif a == '3':
                    if Q_outObj.full():
                        Q_outObj.get()
                    Q_outObj.put(msg)
                    
        

    if (time.time() > oldTimer + 60):
        uart.write("01"+dev_eui.lower()+"\n")
        oldTimer = time.time()
    sendBuffer = struct.pack('i', idTramme)


