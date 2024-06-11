import base64
import struct
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import json
import time

mqtt_username = "dem@ttn"
password = "NNSXS.I2HKSPE36TEGQ7OOR5JCNINKTJTYESZAGJYHANQ.MG6VOHTD66I7JHPIJ5JYHTIQWO5NS47FEVZ3QNNY2TDI6MNPXBTA"
device_name = "lopy4"
topics=['v3/'+mqtt_username+'/devices/'+device_name+'/up']
topicsdown=['v3/'+mqtt_username+'/devices/'+device_name+'/down/push']
auth={'username':mqtt_username,'password':password}
hostname="eu1.cloud.thethings.network"
port = 1883

def send(data ,f_port=1 ):
    data = base64.b64encode(data)
    data=data.decode()
    publish.single(topicsdown[0], '{"downlinks":[{"f_port": '+str(f_port)+',"frm_payload":"'+ data+'","priority": "NORMAL"}]}', hostname=hostname, port=port, auth=auth)




def recieve():
    m = subscribe.simple(topics, hostname=hostname, port=port, auth=auth, msg_count=1)

    message = json.loads(m.payload)
    data = message['uplink_message']['frm_payload']
    data = base64.b64decode(data.encode())
    data=data.hex()
    return data

def send_int(data : int):
    send(bytes([data]),2)

def send_float(data : float):
    send(struct.pack("f", data),3)

def send_str(data : str):
    send(data.encode(),4)



while 1 :
    
    data=recieve()
    
    print(data)

    
    send_int(4)
    send_float(0.2)
    send_str("coucou")
    time.sleep(5)


print("fini")

