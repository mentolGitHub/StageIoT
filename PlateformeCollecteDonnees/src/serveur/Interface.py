import mysql.connector.abstracts
import base64
import json
from queue import Queue
import time
import utils
import datetime

db : mysql.connector.MySQLConnection
db_cursor : mysql.connector.abstracts.MySQLCursorAbstract

data_format = { 'timestamp':"", 'luminosite':None, 'pression':None, 'temperature':None,
                'longitude':None, 'latitude':None, 'altitude':None, 'angle':None, 
                'vitesse_angulaire_X':None, 'vitesse_angulaire_Y':None, 'vitesse_angulaire_Z':None,
                'acceleration_X':None, 'acceleration_Y':None, 'acceleration_Z':None,
                'azimut':None, 'distance_recul':None, 'presence':None , 'humidite':None }

def save_DB(data,id=0):
    global db, db_cursor
    try :
        # db_cursor.execute("show tables")
        # print(db_cursor)
        # utils.print_SQL_response(db_cursor)

        table = "Data"
        db_cursor.execute("SELECT * FROM "+table+" WHERE timestamp = %(timestamp)s;",data)
        
        if db_cursor.arraysize == 2:
            utils.print_SQL_response(db_cursor)
            query=""
            match id :
                case 0 :
                    pass
                case 1 :
                    query = "UPDATE "+ table +" SET data=%(data)s WHERE timestamp=%(timestamp)s"
                case 2 :
                    query = "UPDATE "+ table +" SET gps=Point(%(longitude)s, %(latitude)s),\
                        altitude=%(altitude)s, angle=%(angle)s WHERE timestamp=%(timestamp)s"
                case 3 :
                    query = "UPDATE "+ table +" SET vitesse_angulaire_X=%(vitesse_angulaire_X)s , vitesse_angulaire_Y=%(vitesse_angulaire_Y)s ,\
                        vitesse_angulaire_Z=%(vitesse_angulaire_Z)s ,  pression=%(pression)s WHERE timestamp=%(timestamp)s"
                case 4 :
                    query = "UPDATE "+ table +" SET acceleration_X=%(acceleration_X)s, acceleration_Y=%(acceleration_Y)s,\
                        acceleration_Z=%(acceleration_Z)s, temperature=%(temperature)s WHERE timestamp=%(timestamp)s"
                case 5 :
                    query = "UPDATE "+ table +" SET azimut=%(azimut)s , distance_recul=%(distance_recul)s, presence=%(presence)s ,\
                        luminosity=%(luminosite)s ,  humidity=%(humidite)s WHERE timestamp=%(timestamp)s"
                
            
        else :
            query = "INSERT INTO "+ table +" (timestamp, temperature, humidity, luminosity,\
                    presence, pression, gps, altitude, angle, \
                    vitesse_angulaire_X, vitesse_angulaire_Y, vitesse_angulaire_Z,\
                    azimut, distance_recul) \
                    VALUES (%(timestamp)s, %(temperature)s, %(humidite)s, %(luminosite)s,\
                    %(presence)s, %(pression)s, Point(%(longitude)s, %(latitude)s), %(altitude)s, %(angle)s,\
                    %(vitesse_angulaire_X)s, %(vitesse_angulaire_Y)s, %(vitesse_angulaire_Z)s, %(azimut)s, %(distance_recul)s);"
        # print(query,data)
        
        db_cursor.execute(query,data)
        #print(db_cursor)
        db.commit()
    except ValueError as e :
        print(e)

def data_LoRa_handler(message):
    # try :
    #     data = json.loads(message)
    #     save_DB(data)
    # except json.decoder.JSONDecodeError as e :
        

    try :
        id = int(message[0],base=16)
        data = message[1:]
        values = data.split(",")
        data = data_format
        t=datetime.datetime.fromtimestamp(int(values[0])/1000)
        
        #print(t)
        match id : 
            case 0 :
                data['timestamp']=t
                #TODO: créer des messages systemes, etc

            case 1 :
                data={'timestamp':t, 'data':values[1]}
                #TODO: recuperer les messages personalisés

            case 2 :
                data['timestamp']=t
                data['latitude']=float(values[1])
                data['longitude']=float(values[2])
                data['altitude']=float(values[3])
                data['luminosite']=float(values[4])
                data['vitesse_angulaire_X']=float(values[5])
                data['vitesse_angulaire_Y']=float(values[6])
                data['vitesse_angulaire_Z']=float(values[7])
                if values[8]!='0':
                    data['pression']=float(values[8])
                data['acceleration_X']=float(values[9])
                data['acceleration_Y']=float(values[10])
                data['acceleration_Z']=float(values[11])
                data['angle']=float(values[12])
                data['azimut']=float(values[13])

            # case 3 :
            #     data['timestamp']=t
            #     data['vitesse_angulaire_X']=values[1]
            #     data['vitesse_angulaire_Y']=values[2]
            #     data['vitesse_angulaire_Z']=values[3]
            #     data['pression']=values[4]

            # case 4 :
            #     data['timestamp']=t
            #     data['acceleration_X']=values[1]
            #     data['acceleration_Y']=values[2]
            #     data['acceleration_Z']=values[3]
            #     data['temperature']=values[4]

            # case 5 :
            #     data['timestamp']=t
            #     data['azimut']=values[1]
            #     data['distance recul']=values[2]
            #     data['presence']=values[3]
            #     data['luminosite']=values[4]
            #     data['humidite']=values[5]

            case _ :
                #TODO : raise an error
                print("Wrong format")

        if id in range(0,16):
            #print(data)
            save_DB(data,id)
    except ValueError as e :
        print(message)
        print(e)

def LoRa_msg_handler(msg):
    try :
        message = json.loads(msg.payload)
        
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
                data_LoRa_handler(data)
    except (RuntimeError,KeyError) as e :
        print(msg.payload)
        print(e)

def IP_msg_handler(msg):
    # print(msg)

    data = data_format
    for key in msg.keys():
        data[key]=msg[key]
    data['timestamp']= datetime.datetime.fromtimestamp(int(data['timestamp'])/1000)
    # print(data)
    save_DB(data)
    
    


def Ifnode(Q_Lora : Queue, Q_4G : Queue, Config):
    global db, db_cursor
    print("Starting If node")
    
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