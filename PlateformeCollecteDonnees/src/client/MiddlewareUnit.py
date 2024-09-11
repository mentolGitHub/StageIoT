import datetime
import sys
import time
import serial

uartLoRa = serial.Serial()
uartLTE = serial.Serial()
LoRa_eui = ""

data_format = { 'timestamp':"", 'luminosity':None, 'pression':None, 'temperature':None,
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
        try :
            date = str(datetime.datetime.timestamp(Data["timestamp"]))
        except:
            date = str(datetime.datetime.timestamp(datetime.datetime.now()))
        messages.append("2"+date+","+Data["latitude"]+","+Data["longitude"]+","+Data["altitude"]+"," \
                    +Data["luminosity"]+","+Data["vitesse_angulaire_X"]+","+Data["vitesse_angulaire_Y"]+","+Data["vitesse_angulaire_Z"]\
                    +","+Data["pression"]+","+Data["acceleration_X"]+","+Data["acceleration_Y"]+","+Data["acceleration_Z"]\
                    +","+Data["angle"]+","+Data["azimuth"]+ ","+Data["distance_recul"]+","+Data["humidite"]+","+Data["temperature"])
    if "Object" in Data:
        date = str(datetime.datetime.timestamp(datetime.datetime.now()))
        messages = []
        msg = "3"+date+";"
        for obj in Data["Object"]:
            msg += obj["X"]+","+obj["Y"]+","+obj["Z"]+","+obj["objetLabel"]+";"
        messages.append(msg)
    return messages

def MsgToData(msg):
    """
    Takes the msg and puts it in a Data format
    """

    
    Data = data_format
    if msg[0] == "3":
        objects = msg.strip("\n").split(";")[:-1]
        Data["Object"] = []
        for i in objects:
            i = i[1:].split(",")
            obj = {"X":i[0],"Y":i[1],"Z":i[2],"objetLabel":i[3]}
            Data["Object"].append(obj)
    else :
        msg = msg.decode('utf-8').strip("\n").split(",")
        if msg[0] == "s":
            Data["timestamp"] = msg[1]
            Data["latitude"] = msg[2]
            Data["longitude"] = msg[3]
            Data["altitude"] = msg[4]
            Data["luminosity"] = msg[5]
            Data["vitesse_angulaire_X"] = msg[6]
            Data["vitesse_angulaire_Y"] = msg[7]
            Data["vitesse_angulaire_Z"] = msg[8]
            Data["pression"] = msg[9]
            Data["acceleration_X"] = msg[10]
            Data["acceleration_Y"] = msg[11]
            Data["acceleration_Z"] = msg[12]
            Data["angle"] = msg[13]
            Data["azimuth"] = msg[14]
            Data["distance_recul"] = "0"
            Data["humidite"] = "0"
            Data["temperature"] = "0"
    
    return Data

def UartWriteLoRa(Data):

    """
    Writes the Data packet on the LoRa Uart to send it on the LoRa network
    """

    messages = DataToMsg(Data)
    for msg in messages:
        uartLoRa.write((msg+"\n").encode('utf-8'))
        print(msg)
    

def UartWriteLTE(Data):

    """
    Writes the Data packet on the LTE Uart to send it online
    """

    messages = DataToMsg(Data)
    for msg in messages:
        uartLTE.write((msg+"\n").encode('utf-8'))
        print(msg)


def Middlewarenode(Q_capteurs, Config):

    """
    This is the Middleware node, it sets the right uart interface through the config file and retrives all data comming through the sensor Uart.
    """


    global uartLoRa, uartLTE
    uartLoRa= serial.Serial("/dev/tty"+Config["LoRaUartIF"],115200)
    uartLTE= serial.Serial("/dev/tty"+Config["LTEUartIF"],115200)
    uartSensor= serial.Serial("/dev/tty"+Config["SensorUartIF"], 115200)
    try:
        while True:
            msg = uartSensor.readline()
            try :
                if (msg.decode('utf-8')[:4] == "LoRa"):
                    LoRa_eui = msg.decode('utf-8')[4:]
                else :            
                    data = MsgToData(msg)
                    
                    Q_capteurs.put(data)
            except Exception as e:
                print(e)
            
    except KeyboardInterrupt :
        print("Middleware Stopped")
        sys.exit(0) 