import base64
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import json

topics=['v3/dem@ttn/devices/lopy4/up']
topicsdown=['v3/dem@ttn/devices/lopy4/down/push']
auth={'username':"dem@ttn",'password':"NNSXS.I2HKSPE36TEGQ7OOR5JCNINKTJTYESZAGJYHANQ.MG6VOHTD66I7JHPIJ5JYHTIQWO5NS47FEVZ3QNNY2TDI6MNPXBTA"}
hostname="eu1.cloud.thethings.network"
port = 1883

while 1 :
    m = subscribe.simple(topics, hostname=hostname, port=port, auth=auth, msg_count=1)

    message = json.loads(m.payload)
    data = message['uplink_message']['frm_payload']
    print(data)
    data = base64.b64decode(data.encode())
    data=data.hex()
    print(data)


    data="coucou"
    data = base64.b64encode(data.encode())
    data=data.decode()
    publish.single(topicsdown[0], '{"downlinks":[{"f_port": 15,"frm_payload":"'+ data+'","priority": "NORMAL"}]}', hostname=hostname, port=port, auth=auth)


print("fini")

