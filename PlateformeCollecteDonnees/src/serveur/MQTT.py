import base64
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import json
import time

topics=['v3/stm32LoRa@ttn/devices/eui-713bd57ed00681e2/up']
topicsdown=['v3/stm32LoRa@ttn/devices/eui-713bd57ed00681e2/down/push']
auth={'username':"stm32LoRa@ttn",'password':"NNSXS.F4WRQ3VRWAU7PVPZISAL5AN3Q3KQLNMJDTPQQGA.U3YCIM76SZONPLF62J62FTNMVRWM2QUO3QGHEHZX67XJXVK2L7MQ"}
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

    
    #send(data)
    time.sleep(0.5)


print("fini")

