import base64
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import json
import time

import mysql



def receive_callback(msg):
    print(msg)

def api_callback(cmd):
    print(cmd)



def init_db():
    mydb = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword"
    )

    print(mydb) 

def init_config():
    open("config.conf")
    

def init_server():
    init_config()
    init_db()
    


def main():
    init_server()





if __name__ == "__main__":
    main()



