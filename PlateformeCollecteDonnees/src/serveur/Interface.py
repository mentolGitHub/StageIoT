import mysql.connector.abstracts
import base64
import json
from queue import Queue
import time
import utils
import datetime
import requests

db : mysql.connector.MySQLConnection
db_cursor : mysql.connector.abstracts.MySQLCursorAbstract
Config = {}
data_format = { 'eui' : None, 'timestamp':"", 'luminosity':None, 'pression':None, 'temperature':None,
                'longitude':None, 'latitude':None, 'altitude':None, 'angle':None, 
                'vitesse_angulaire_X':None, 'vitesse_angulaire_Y':None, 'vitesse_angulaire_Z':None,
                'acceleration_X':None, 'acceleration_Y':None, 'acceleration_Z':None,
                'azimuth':None, 'distance_recul':None, 'presence':None , 'humidite':None,  'distance_recul':None}


def save_DB(data,id=0):
    global db, db_cursor
    try :
        # db_cursor.execute("show tables")
        # print(db_cursor)
        # utils.print_SQL_response(db_cursor)
        
        data['timestamp']=datetime.datetime.fromtimestamp(data['timestamp'])
        table = "Data"
        db_cursor.execute("SELECT * FROM "+table+" WHERE timestamp = %(timestamp)s",data)
        
        if db_cursor.rowcount >= 1:
            utils.print_SQL_response(db_cursor)
            query=""
            match id :
                case 0 :
                    pass
                
        else :
            match id :
                case 2 :
                    
                    query = "INSERT INTO "+ table +" (timestamp, temperature, humidity, luminosity,\
                            presence, pression, longitude, latitude, altitude, angle, \
                            vitesse_angulaire_X, vitesse_angulaire_Y, vitesse_angulaire_Z,\
                            acceleration_X, acceleration_Y,acceleration_Z,\
                            azimuth, distance_recul, source) \
                            VALUES (%(timestamp)s, %(temperature)s, %(humidite)s, %(luminosity)s,\
                            %(presence)s, %(pression)s, %(longitude)s, %(latitude)s, %(altitude)s, %(angle)s,\
                            %(vitesse_angulaire_X)s, %(vitesse_angulaire_Y)s, %(vitesse_angulaire_Z)s,%(acceleration_X)s,\
                            %(acceleration_Y)s,%(acceleration_Z)s, %(azimuth)s, %(distance_recul)s, %(eui)s)"
                    
                case 3 :
                    table = "Obstacles"
                    query = "INSERT INTO "+ table +" "
                    
        # print(query,data)
        # print(data)
        db_cursor.execute(query,data)
        #print(db_cursor)
        db.commit()
    except ValueError as e :
        print(e)

def data_LoRa_handler(message,device):
    id = int(message[0],base=16)
    message = message[0]+device+"," + message[1:]
    
    # print(message)
    if id in range(0,16):
        #print(data)
        requests.post("http://"+Config['server_host']+":"+Config['server_port']+"/post_data",data=message)
        # save_DB(data,id)


def LoRa_msg_handler(msg):
    try :
        message = json.loads(msg.payload)
        # print(msg.topic)
        #print(msg.payload)
        type = msg.topic.split("/")[-1]
        match type : 
            case "join":
                device = message['end_device_ids']['device_id']
                print(device)
            case "up":
                data = message['uplink_message']['frm_payload']
                data = base64.b64decode(data.encode())
                try :
                    data = data.decode()
                except UnicodeDecodeError :
                    data = data.hex()
                #print(data)
                data_LoRa_handler(data,msg.topic.split("/")[3].split("-")[-1])
    except (RuntimeError,KeyError) as e :
        print(msg.payload)
        print(e)

def IP_msg_handler(msg):
    # print(msg)

    data = data_format
    for key in msg.keys():
        data[key]=msg[key]
    data['timestamp']= int(data['timestamp'])/1000
    # print(data)
    assert(data['timestamp']<=datetime.datetime.now().timestamp())
    db=mysql.connector.connect(host="localhost", user=Config["SQL_username"], database=Config["db_name"])
    cursor=db.cursor(buffered=True)

    device = data["eui"]
    query = "SELECT * FROM Device WHERE `dev-eui`=%s"
    cursor.execute(query,(device,))
    res = cursor.fetchall()
    # print(res)
    if len(res)!=0:
        save_DB(data)
    else:
        print("device "+device+" not registered")
    
    


def Ifnode(Q_Lora : Queue, Q_4G : Queue, Config_):
    global db, db_cursor, Config
    print("Starting If node")
    Config=Config_
    db = mysql.connector.connect(host="localhost", user=Config["SQL_username"])
    db_cursor = db.cursor(buffered=True)
    db_query = "USE "+ utils.sql_var(Config["db_name"])
    db_cursor.execute(db_query)
    
    while True:
        while Q_Lora.empty() and Q_4G.empty():
            time.sleep(0.002)
        if not Q_Lora.empty():
            message = Q_Lora.get()
            LoRa_msg_handler(message)
        if not Q_4G.empty():
            message = Q_4G.get()
            # print(message)
            IP_msg_handler(message)