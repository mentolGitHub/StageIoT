import base64
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import json
import time

mqtt_username = ""
password = ""
device_name = ""
topics=['v3/'+mqtt_username+'/devices/'+device_name+'/up']
topicsdown=['v3/'+mqtt_username+'/devices/'+device_name+'/down/push']
auth={'username':mqtt_username,'password':password}
hostname="eu1.cloud.thethings.network"
port = 1883

def send(data):
    data = base64.b64encode(data.encode())
    data=data.decode()
    publish.single(topicsdown[0], '{"downlinks":[{"f_port": 15,"frm_payload":"'+ data+'","priority": "NORMAL"}]}', hostname=hostname, port=port, auth=auth)

def recieve():
    m = subscribe.simple(topics, hostname=hostname, port=port, auth=auth, msg_count=1)

    message = json.loads(m.payload)
    data = message['uplink_message']['frm_payload']
    data = base64.b64decode(data.encode())
    data=data.hex()
    return data






while 1 :
   
    data=recieve()
    
    print(data)

    
    send(data)
    time.sleep(0.5)


print("fini")

