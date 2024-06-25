import mysql.connector.abstracts
import base64
import json
from queue import Queue
import time
import utils

db_cursor : mysql.connector.abstracts.MySQLCursorAbstract

data_format = { 'timestamp':"", 'luminosite':None, 'pression':None, 'temperature':None,
                'longitude':None, 'latitude':None, 'altitude':None, 'angle':None, 
                'vitesse angulaire X':None, 'vitesse angulaire Y':None, 'vitesse angulaire Z':None,
                'azimut':None, 'distance recul':None, 'presence':None , 'humidite':None }

def save_DB(data):
    table = "Data"
    db_cursor.execute("SELECT * FROM "+table+" WHERE unique_key = %(timestamp)s;",data)
    utils.print_SQL_response(db_cursor)

    return

    if data_exist :
        query = "UPDATE "+ table +" SET = %()s, =%()s, =%()s WHERE timestamp=%(timestamp)s"

        db_cursor.execute()
    else :
        query = "INSERT INTO"


    # 
    query = "INSERT INTO "+ table +" (timestamp, temperature, humidity, luminosity,\
            presence, pression, longitude, latitude, altitude, angle, \
            vitesse angulaire X, vitesse angulaire Y, vitesse angulaire Z,\
            azimut, distance recul, humidite) \
            VALUES (%(timestamp)s, %(temperature)s, %(humidite)s, %(luminosite)s, %(presence)s, %(pression)s, %()s)"
    
    db_cursor.execute(query,data)
    

def data_LoRa_handler(message):
    try :
        id = int(message[0],base=16)
        data = message[1:]
        values = data.split(",")
        print(time.localtime())
        data = data_format
        match id : 
            case 0 :
                data['timestamp']=values[0]
                #TODO: créer des messages systemes, etc

            case 1 :
                
                data['timestamp']=values[0]
                #TODO: recuperer les messages personalisés

            case 2 :
                
                data['timestamp']=values[0]
                data['longitude']=values[1]
                data['latitude']=values[2]
                data['altitude']=values[3]
                data['angle']=values[4]

            case 3 :
                data['timestamp']=values[0]
                data['vitesse angulaire X']=values[1]
                data['vitesse angulaire Y']=values[2]
                data['vitesse angulaire Z']=values[3]
                data['pression']=values[4]

            case 4 :
                data['timestamp']=values[0]
                data['accelération X']=values[1]
                data['accelération Y']=values[2]
                data['accelération Z']=values[3]
                data['temperature']=values[4]

            case 5 :
                data['timestamp']=values[0]
                data['azimut']=values[1]
                data['distance recul']=values[2]
                data['presence']=values[3]
                data['luminosite']=values[4]
                data['humidite']=values[5]

            case _ :
                #TODO : raise an error
                print("Wrong format")
                
        if not id in range(0,16):
            save_DB(data)
    except ValueError as e :
        print(e)

def LoRa_msg_handler(msg):
    message = json.loads(msg.payload)
    
    print(msg.topic)
    type = msg.topic.split("/")[-1]
    match type : 
        case "join":
            device = message['end_device_ids']['device_id']
            print(device)
        case "up":
            data = message['uplink_message']['frm_payload']
            data = base64.b64decode(data.encode())
            data=data.hex()
            print(data)
            data_LoRa_handler(data)

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