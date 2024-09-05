import datetime
from queue import Queue
import time
import mysql.connector
import mysql.connector.abstracts
import sys
import uuid
from MiddlewareUnit import MsgToData

db : mysql.connector.MySQLConnection
db_cursor : mysql.connector.abstracts.MySQLCursorAbstract
db_cursor_object : mysql.connector.abstracts.MySQLCursorAbstract
data_format = { 'timestamp':"", 'luminosity':None, 'pression':None, 'temperature':None,
                'longitude':None, 'latitude':None, 'altitude':None, 'angle':None, 
                'vitesse_angulaire_X':None, 'vitesse_angulaire_Y':None, 'vitesse_angulaire_Z':None,
                'acceleration_X':None, 'acceleration_Y':None, 'acceleration_Z':None,
                'azimuth':None, 'distance_recul':None, 'presence':None , 'humidite':None,  'distance_recul':None}

def save_DB(data):

    """
    Saves the Data in the local DB with format relative to the msg ID
    """
    
    try :
        data['timestamp']=datetime.datetime.fromtimestamp(int(data['timestamp'])/1000)

        table = "Data"
        query = "INSERT INTO "+ table +" (timestamp, temperature, humidity, luminosity,\
                presence, pression, longitude, latitude, altitude, angle, \
                vitesse_angulaire_X, vitesse_angulaire_Y, vitesse_angulaire_Z,\
                acceleration_X, acceleration_Y,acceleration_Z,\
                azimuth, distance_recul) \
                VALUES (%(timestamp)s, %(temperature)s, %(humidite)s, %(luminosity)s,\
                %(presence)s, %(pression)s, %(longitude)s, %(latitude)s, %(altitude)s, %(angle)s,\
                %(vitesse_angulaire_X)s, %(vitesse_angulaire_Y)s, %(vitesse_angulaire_Z)s,%(acceleration_X)s,\
                %(acceleration_Y)s,%(acceleration_Z)s, %(azimuth)s, %(distance_recul)s)"
        print (data)
        if 'Object' in data:
            data.pop('Object')
        db_cursor.execute(query,data)
        db.commit()
        
    except ValueError as e :
        print(e)

def save_object_DB(data):

    """
    Save objects into the database
    """
    try :
        #timestamp d'aujourd'hui
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        data = data['Object']
        for i in data :
            i['timestamp']=timestamp
            table = "Objets"
            query = "INSERT INTO "+ table +" (timestamp, X, Y, Z, label) \
                    VALUES (%(timestamp)s, %(X)s, %(Y)s, %(Z)s, %(objetLabel)s)"
            db_cursor_object.execute(query,i)
            db.commit()
        
    except ValueError as e :
        print(e)

def dataCollectornode(Q_input : Queue, Q_input_objects : Queue, Q_output : Queue, Q_send_serv : Queue, conf, db_, cursor):

    """
    This is the DataCollector node, it retrives all Data from sensors, saves it localy and sends it to the network unit.
    """

    print("collect data actif")

    # setup DB locale
    global Config, db, db_cursor, db_cursor_object
    Config = conf
    db = db_
    db_cursor=cursor
    db_cursor_object=cursor
    try:
        while True:

            data = {}
            while Q_input.empty() and Q_input_objects.empty():
                time.sleep(0.002)
            if not Q_input.empty():
                data = Q_input.get()

                save_DB(data)
                Q_send_serv.put(data)
                #Q_output.put(data) #optional output
            if not Q_input_objects.empty():
                data = Q_input_objects.get()
                data = MsgToData(data)
                save_object_DB(data)
                Q_send_serv.put(data)
                #Q_output.put(data) #optional

    except KeyboardInterrupt :
        sys.exit(0)
    