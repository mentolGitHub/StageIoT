from network import Bluetooth
from machine import Timer

def char_notify_callback(char):
    char_value = (char.value())
    print("New value: {}".format(char_value))

bt = Bluetooth()
print('Start scanning for BLE services')
bt.start_scan(-1)
adv = None
while(True):
    adv = bt.get_adv()
    if adv:
        print(adv)
        print(bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL))
        print(bt.resolve_adv_data(adv.mac, Bluetooth.ADV_MAC))
        try:
            if bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)=="FiPy 45":
                conn = bt.connect(adv.mac)
                print("Connected")
                try:
                    services = conn.services()
                    for service in services:
                        chars = service.characteristics()
                        for char in chars:
                            c_uuid = char.uuid()
                            if (char.properties() & Bluetooth.PROP_NOTIFY):
                                char.callback(trigger=Bluetooth.CHAR_NOTIFY_EVENT, handler=char_notify_callback)
                                print("uuid"+str(c_uuid))
                                break
                except:
                    continue
        except:
            continue

bt.stop_scan()
bt.disconnect_client()
