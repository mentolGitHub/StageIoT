import sys
import time
import serial

uartLoRa = serial.Serial()
uartLTE = serial.Serial()

data_format = { 'eui' : None, 'timestamp':"", 'luminosity':None, 'pression':None, 'temperature':None,
                'longitude':None, 'latitude':None, 'altitude':None, 'angle':None, 
                'vitesse_angulaire_X':None, 'vitesse_angulaire_Y':None, 'vitesse_angulaire_Z':None,
                'acceleration_X':None, 'acceleration_Y':None, 'acceleration_Z':None,
                'azimuth':None, 'distance_recul':None, 'presence':None , 'humidite':None,  'distance_recul':None}


def DataToMsg(Data):

    """
    Takes the Data and puts it in a string format for Uart and LoRa (also LTE But wouldnt have been necessary)
    """

    messages = []
    if Data["timestamp"] != "" : 
        messages.append("2"+Data["timestamp"]+","+Data["latitude"]+","+Data["longitude"]+","+Data["altitude"]+"," \
                    +Data["luminosity"]+","+Data["vitesse_angulaire_X"]+","+Data["vitesse_angulaire_Y"]+","+Data["vitesse_angulaire_Z"]\
                    +","+Data["pression"]+","+Data["acceleration_X"]+","+Data["acceleration_Y"]+","+Data["acceleration_Z"]\
                    +","+Data["angle"]+","+","+Data["azimuth"]+ ","+Data["distance_recul"]+","+Data["humidite"]+","+Data["temperature"])
    if Data["Object"] != None :
        for obj in Data["Object"]:
            messages.append("3"+obj["X"]+","+Data["Y"]+","+Data["Z"]+","+Data["objetLabel"])#....
    return messages

def UartWriteLoRa(Data):

    """
    Writes the Data packet on the LoRa Uart to send it on the LoRa network
    """

    messages = DataToMsg(Data)
    for msg in messages:
        uartLoRa.write(msg)
    

def UartWriteLTE(Data):

    """
    Writes the Data packet on the LTE Uart to send it online
    """

    messages = DataToMsg(Data)
    for msg in messages:
        uartLTE.write(msg)



def Middlewarenode(Q_capteurs, Config):

    """
    This is the Middleware node, it sets the right uart interface through the config file and retrives all data comming through the sensor Uart.
    """


    global uartLoRa, uartLTE
    uartLoRa= serial.Serial("/dev/tty"+Config["LoRaUartIF"])
    uartLTE= serial.Serial("/dev/tty"+Config["LTEUartIF"])
    uartSensor= serial.Serial("/dev/tty"+Config["CapUartIF"])
    try:
        while True:
            msg = uartSensor.readline()
            print(msg)
                
            
    except KeyboardInterrupt :
        sys.exit(0)