import mysql.connector.abstracts
import base64
import json
from queue import Queue
import time

db_cursor : mysql.connector.abstracts.MySQLCursorAbstract

def save_DB(data):
    t=data['timestamp']
    pos=data['position']
    lum=data['lumiosité']
    pressure=data['pression']

    # make sure the data is conforme
    return


    # 
    table = "Data"
    query = "INSERT INTO "+ table +" (timestamp, position, luminosité, pression) VALUES (%s, %s, %s, %s)"
    args=(t,pos,lum,pressure)
    db_cursor.execute(query,args)
    

def data_handler(message):
    if message[0]=='{':
        data = json.loads(message)
        print(data)
        save_DB(data)

def LoRa_msg_handler(msg):
    message = json.loads(msg.payload)
    
    # print(msg.topic)
    type = msg.topic.split("/")[-1]
    match type : 
        case "join":
            device = message['end_device_ids']['device_id']
            print(device)
        case "up":
            data = message['uplink_message']['frm_payload']
            data = base64.b64decode(data.encode())
            data=data.hex()
            #print(data)
            data_handler(data)

def LTE_msg_handler(msg):
    print(msg)
    


def Ifnode(Q_Lora : Queue, Q_4G : Queue, cursor : mysql.connector.abstracts.MySQLCursorAbstract):
    global db_cursor
    print("Starting If node")
    db_cursor = cursor
    while True:
        while Q_Lora.empty() and Q_4G.empty():
            time.sleep(0.1)
        if not Q_Lora.empty():
            message = Q_Lora.get()
            LoRa_msg_handler(message)
        if not Q_4G.empty():
            message = Q_4G.get()
            LTE_msg_handler(message)