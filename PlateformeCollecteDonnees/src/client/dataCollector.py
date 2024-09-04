import datetime
from queue import Queue
import time
import mysql.connector
import mysql.connector.abstracts
import sys

db : mysql.connector.MySQLConnection
db_cursor : mysql.connector.abstracts.MySQLCursorAbstract
data_format = { 'eui' : None, 'timestamp':"", 'luminosity':None, 'pression':None, 'temperature':None,
                'longitude':None, 'latitude':None, 'altitude':None, 'angle':None, 
                'vitesse_angulaire_X':None, 'vitesse_angulaire_Y':None, 'vitesse_angulaire_Z':None,
                'acceleration_X':None, 'acceleration_Y':None, 'acceleration_Z':None,
                'azimuth':None, 'distance_recul':None, 'presence':None , 'humidite':None,  'distance_recul':None}

def save_DB(data):

    """
    Saves the Data in the local DB with format relative to the msg ID
    """
    
    try :
        data['timestamp']=datetime.datetime.fromtimestamp(data['timestamp'])
        
                
        
        match id :
            case 2 :
                table = "Data"
                db_cursor.execute("SELECT * FROM "+table+" WHERE timestamp = %(timestamp)s",data)
                
                if db_cursor.rowcount >= 1:
                    pass
                else :
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
                pass
        db_cursor.execute(query,data)
        #print(db_cursor)
        db.commit()
    except ValueError as e :
        print(e)


def dataCollectornode(Q_input : Queue, Q_output : Queue, Q_send_serv : Queue, conf, db_, cursor):

    """
    This is the DataCollector node, it retrives all Data from sensors, saves it localy and sends it to the network unit.
    """

    # setup DB locale
    global Config, db, db_cursor
    Config = conf
    db = db_
    db_cursor=cursor
    try:
        while True:

            data = {}
            while Q_input.empty() :
                time.sleep(0.002)
            if not Q_input.empty():
                data = Q_input.get()


                save_DB(data)
                Q_send_serv.put(data)
                #Q_output.put(data) #optional output

    except KeyboardInterrupt :
        sys.exit(0)
    