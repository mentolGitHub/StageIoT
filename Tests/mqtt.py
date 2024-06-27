import base64
import struct
import sys
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import json
import time

mqtt_username = "stm32lora1@ttn"
password = "NNSXS.U6KN7IY6K2MWWA54MKJVCON3BFH2B4GNBVYC7VY.F33QNU3IFQ63X7XOBVHS7AU4O2DA4MPPC6M3EXXTEZHKGSZAUALA"
device_name = "eui-70b3d57ed006898c"
topics=['v3/'+mqtt_username+'/devices/'+device_name+'/up']
topicsdown=['v3/'+mqtt_username+'/devices/'+device_name+'/down/push']
auth={'username':mqtt_username,'password':password}
hostname="eu1.cloud.thethings.network"
port =8883



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





# while 1 :
   
#     data=recieve()
    
#     print(data)

    
#     #send(data)
#     time.sleep(0.5)


# print("fini")

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def on_subscribe(mqttc, obj, mid, granted_qos, arg):
    print("\nSubscribe: " + str(mid) + " " + str(granted_qos))

def MQTTnode():
    print("Starting MQTT node")

    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.on_subscribe = on_subscribe
    mqttc.username_pw_set(username=mqtt_username, password=password)
    #connection securisé entre le serveur TTN et le serveur (client MQTT)
    mqttc.tls_set()	# default certification authority of the system
    mqttc.connect(hostname,port,60)
    mqttc.subscribe("#", 0)	# all device uplinks
    
    mqttc.loop_forever()
    

MQTTnode()