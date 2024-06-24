import base64
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import json
import time
import threading
import mysql.connector
import Interface
import MQTT
import utils

Config={"db_name":"plateformeIot"}

def receive_callback(msg):
    print(msg)

def api_callback(cmd):
    print(cmd)



def init_db():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root"
    )
    cursor = mydb.cursor()
    
    # Recherche de la DB
    liste_db=[]
    cursor.execute("SHOW DATABASES LIKE %s;", (Config["db_name"],))
    for i in cursor:
        liste_db+=i

    print(liste_db)
    if len(liste_db)== 1:
        db_query = "USE "+ Config["db_name"]
        cursor.execute(db_query)
    elif len(liste_db)==0:
        print("Aucune base de données de ce nom n'a été trouvé. Voulez vous la créer ? [y/n] :")
        print("Pas encore implémenté")
    
    # Import des tables (si elles n'existent pas)
    path_setup_DB = "stageiot.sql"
    sql=open(path_setup_DB).read()
    cursor.execute(sql)
    utils.print_SQL_response(cursor)





def init_config():
    conf = open("config.conf")
    
    # parse chaque ligne
    for ligne in conf:
        # '=' est le centre du message avec key '=' value
        if "=" in ligne:
            k,v=ligne.split("=")
            v= v.strip() # on retire les espaces
            for key in Config.keys():
                # si la clé est dans les clé de la Config on associe la valeur
                if k==key and v!="":
                    Config[key]=v
                
    print(Config)

def init_server():
    init_config()
    init_db()
    
def run_server():
    threadMQTT = threading.Thread(target=MQTT.MQTTnode)
    threadIf = threading.Thread(target=Interface.Ifnode)
    threadMQTT.start()
    while threading.active_count()>1:
        time.sleep(1)

def main():
    init_server()

    run_server()


if __name__ == "__main__":
    main()



