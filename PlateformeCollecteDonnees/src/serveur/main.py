import time
import threading
import mysql.connector
import mysql.connector.abstracts

import Interface
import MQTT
import utils
from queue import Queue

Config={"db_name":"plateformeIot"}
db_Cursor : mysql.connector.abstracts.MySQLCursorAbstract


def receive_callback(msg):
    print(msg)

def api_callback(cmd):
    print(cmd)



def init_db():
    global db_Cursor
    try : 
        mydb = mysql.connector.connect(
        host="localhost",
        user="root"
        )
        
        cursor = mydb.cursor()
        
        # Seaching for DB
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
        
        # Import tables (if they dont exist yet)
        path_setup_DB = __file__.rsplit("/",1)[0]+"/stageiot.sql"
        sql=open(path_setup_DB).read()
        cursor.execute(sql)
        utils.print_SQL_response(cursor)
        db_Cursor=cursor
    except mysql.connector.errors.ProgrammingError as e :
        print(e)
        exit(1)



def init_config():
    path = __file__.rsplit("/",1)[0]+"/config.conf"
    print(path)
    conf = open(path)
    
    # parsing each line
    for line in conf:
        # '=' is the center of the msg with the syntax : "<key>=<value>"
        if '=' in line:
            k,v=line.split('=')
            v= v.strip() # on retire les espaces
            for key in Config.keys():
                # if the key is in the Config keys we take it's value
                if k==key and v!="":
                    Config[key]=v
                
    print(Config)

def init_server():
    init_config()
    init_db()
    
def run_server():
    #Queues and nodes parameters
    Q_Lora = Queue()
    Q_4G = Queue()
    coordsTTN = ""
    # création des threads
    threadMQTT = threading.Thread(target=MQTT.MQTTnode,args=[coordsTTN,Q_Lora])
    threadIf = threading.Thread(target=Interface.Ifnode,args=[Q_Lora,Q_4G,db_Cursor])

    # start les threads
    threadMQTT.start()
    threadIf.start()


    while threading.active_count()>1:
        time.sleep(1)


def main():
    
    init_server()

    run_server()


if __name__ == "__main__":
    main()



