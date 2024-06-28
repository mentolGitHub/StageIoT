import sys
import time
import threading
from queue import Queue
import mysql.connector
import Interface
import MQTT
import web.IP as IP
import utils

Config={"db_name":"plateformeIot","SQL_username":"root","db_init_file":"stageiot", 
        "APP_username":"stm32lora1@ttn" , "APP_password":"NNSXS.U6KN7IY6K2MWWA54MKJVCON3BFH2B4GNBVYC7VY.F33QNU3IFQ63X7XOBVHS7AU4O2DA4MPPC6M3EXXTEZHKGSZAUALA", 
        "APP_hostname":"eu1.cloud.thethings.network", "APP_port":"8883"}
db : mysql.connector.MySQLConnection

def init_db():

    """
    Initialise the data base. Retreive config info from the dict Config
    Select the db for the data collection plateform.
    Beware that this might not be secure with respect to the config file 
    (cant do secure "USE db" or some other query but there is still a minimal check)
    """

    global db
    try : 
        #connect to mySQL

        mydb = mysql.connector.connect(host="localhost", user=Config["SQL_username"])
        db=mydb
        cursor = mydb.cursor()
        
        # Seaching for DB
        liste_db=[]
        cursor.execute("SHOW DATABASES LIKE %s", (Config["db_name"],))
        for i in cursor:
            liste_db+=i

        #print(liste_db)
        if len(liste_db)== 1:
            db_query = "USE "+ utils.sql_var(Config["db_name"])
            cursor.execute(db_query)

        elif len(liste_db)==0:
            print("Aucune base de données de ce nom n'a été trouvé. Voulez vous la créer ? ", end="")
            valid = False
            while not valid:
                ans = input("[y/n] : ")
                ans = ans.strip(" ")
                ans = ans.strip("-")
                ans = ans.lower()
                if ans in ["y","yes","ye","es"]:
                    valid = True
                    #Create DB
                    query="CREATE database " + utils.sql_var(Config["db_name"])
                    print(query)
                    cursor.execute(query)
                    db_query = "USE "+ utils.sql_var(Config["db_name"])
                    cursor.execute(db_query)
                else :
                    if ans in  ["n","no"]:
                        # Dont create DB -> exit
                        exit(0) 
                    else :
                        print("Veulliez respecter la syntaxe ", end="")
                        
        # Import tables (if they dont exist yet)
        path_setup_DB = __file__.rsplit("/",1)[0]+"/"+Config['db_init_file']+".sql"
        sql=open(path_setup_DB).read()
        cursor.execute(sql)
        utils.print_SQL_response(cursor)
        

    except mysql.connector.errors.ProgrammingError as e :
        print(e)
        exit(1)



def init_config():
    
    """
    Initialise the program Config
    The config file must be in the same folder/directory as the program
    It is not nessecary to enter evey field of the config file as there are default values
    """

    path = __file__.rsplit("/",1)[0]+"/config.conf"
    print(path)
    conf = open(path)
    
    # parsing each line
    for line in conf:
        # '=' is the center of the msg with the syntax : "<key>=<value>"
        if '=' in line:
            k,v=line.split('=')
            v= v.strip() # on retire les espaces
            v.lstrip('"')
            v.rstrip('"')
            for key in Config.keys():
                # if the key is in the Config keys we take it's value
                if k==key and v!="":
                    Config[key]=v
                
    print(Config)

def init_server():

    """
    Initialise the server config and database.
    """

    init_config()
    init_db()
    
def run_server():

    """
    Run the server nodes. A node is a thread with a functionality (it may create other threads that fulfill the same goal.).
    We link the diferents threads with Queues. Thoses represent the channels and we can determine the form of the data with it.
    """

    #Queues and nodes parameters
    Q_Lora = Queue()
    Q_4G = Queue()
    coordsTTN = {
        'mqtt_username' :Config["APP_username"],
        'password' : Config["APP_password"],
        'hostname':Config["APP_hostname"],
        'port' : int(Config["APP_port"])
    }
    # création des threads
    threadMQTT = threading.Thread(target=MQTT.MQTTnode,args=[coordsTTN,Q_Lora])
    threadIf = threading.Thread(target=Interface.Ifnode,args=[Q_Lora,Q_4G,Config])
    threadIP = threading.Thread(target=IP.IPnode,args=[Q_4G,Config])

    # start les threads
    try:
        threadMQTT.start()
        threadIP.start()
        threadIf.start()
        
        # IP.IPnode(Q_4G,Config)

    except (KeyboardInterrupt, SystemExit):
        
        sys.exit()
    


def main():

    """
    This is the main function of the Data Collecting plateform server.
    This program uses a MySQL database.
    You can modify some configuration settings in the config.conf file that is in the same folder/directory as this program.
    DB auth not implemented yet, use a user with no password.
    """

    init_server()
    run_server()


if __name__ == "__main__":
    main()



