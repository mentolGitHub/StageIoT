from queue import Queue
import mysql.connector
import mysql.connector.abstracts
import sys

db : mysql.connector.MySQLConnection
db_cursor : mysql.connector.abstracts.MySQLCursorAbstract

def save_DB(data):
    #TODO:
    table = "Data"
    query = "INSERT INTO "+ table +" (timestamp, temperature, humidity, luminosity,\
            presence, pression, gps, altitude, angle, \
            vitesse_angulaire_X, vitesse_angulaire_Y, vitesse_angulaire_Z,\
            azimut, distance_recul) \
            VALUES (%(timestamp)s, %(temperature)s, %(humidite)s, %(luminosite)s,\
            %(presence)s, %(pression)s, Point(%(longitude)s, %(latitude)s), %(altitude)s, %(angle)s,\
            %(vitesse_angulaire_X)s, %(vitesse_angulaire_Y)s, %(vitesse_angulaire_Z)s, %(azimut)s, %(distance_recul)s);"
    db_cursor.execute(query,data)
    #print(db_cursor)
    db.commit()



def dataCollectornode(listeQ_input : Queue[10], Q_output : Queue, Q_send_serv : Queue, conf, db_, cursor):
    # setup DB locale
    global Config, db, db_cursor
    Config = conf
    db = db_
    db_cursor=cursor
    try:
        while True:
            #TODO:

            data = {}




            save_DB(data)
            Q_send_serv.put(data)
            Q_output.put(data)

            pass
    except KeyboardInterrupt :
        sys.exit(0)
    