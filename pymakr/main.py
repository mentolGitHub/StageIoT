import uos
from network import LoRa
import socket
import time
import ubinascii
import pycom
import utime
from machine import Timer


# create an OTAA authentication parameters, change them to the provided credentials
app_eui = ubinascii.unhexlify('70B3D57ED0038811')
app_key = ubinascii.unhexlify('583FE2F370E3F43BCFE06291DCD155A1')
#uncomment to use LoRaWAN application provided dev_eui
dev_eui = ubinascii.unhexlify('70b3d5499e370b3d')
#parametres LoRa
sf = 7
coding_rate=LoRa.CODING_4_5



pycom.heartbeat(False)
print("=================== Starting program =======================")

chrono = Timer.Chrono()
chrono.start()



def loraWAN():
    def rx_callback(lora):
        lora.events()
        data = s.recv(64)
        if data :
            print(data)

    # Initialise LoRa in LORAWAN mode.
    # Please pick the region that matches where you are using the device:
    # Asia = LoRa.AS923
    # Australia = LoRa.AU915
    # Europe = LoRa.EU868
    # United States = LoRa.US915
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
    
    lora.callback(LoRa.RX_PACKET_EVENT,rx_callback)
    # join a network using OTAA (Over the Air Activation)
    #uncomment below to use LoRaWAN application provided dev_eui
    #lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
    lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)


    # wait until the module has joined the network
    while not lora.has_joined():
        pycom.rgbled(0x101000)
        time.sleep(0.3)
        pycom.rgbled(0x000000)
        time.sleep(0.3)
        

    print('Joined')
    pycom.rgbled(0x001000)
    # create a LoRa socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

    # set the LoRaWAN data rate
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

    # make the socket blocking
    # (waits for the data to be sent and for the 2 receive windows to expire)


    # send some data
    while 1 :
        s.setblocking(True)
        
        s.send(bytes("1","utf-8"))


        time.sleep(3)
        

def loraP2P():
    
    class Stat:
        labels = ('rx_timestamp', 'rssi', 'snr', 'sftx', 'sfrx', 'tx_trials', 'tx_power', 'tx_time_on_air', 'tx_counter', 'tx_frequency')
        nb_moyenne = 0
        stat = [0 for i in labels]
        
        

        def addStats(self, stats):
            self.stat,self.nb_moyenne
            self.stat = [self.stat[x]+stats[x] for x in range(0,len(stats)-1)]
            self.nb_moyenne+=1

        def printStats(self):
            if self.nb_moyenne > 0:
                

                # Lire l'heure actuelle
                time = chrono.read()
                
                sortie = "[time:"+str(time)
                for x in range(0,len(self.stat)-1):
                    sortie += ", " +self.labels[x] +" : "+ str(self.stat[x]/self.nb_moyenne)
                sortie += "]"
                print(sortie)

        
   

    def cb_rx(lora):
        stats = lora.stats()
        nb=nb+1
        stat.addStats(stats)
        if nb == 10:
            stat.printStats()
            nb=0
        pycom.rgbled(0x101000)
        data = s2.recv(64)
        #print(data.decode())
        time.sleep(0.1)
        if(data.decode() == "ping"):
            s2.send("pong")
        elif(data.decode() == "pong"):
            s2.send("ping")
        
        pycom.rgbled(0x001000)

    
    


    stat = Stat()
    nb = 0
    lorap2p = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
    lorap2p.callback(LoRa.RX_PACKET_EVENT, handler=cb_rx)
    lorap2p.init(mode=LoRa.LORA, region=LoRa.EU868,sf=sf,coding_rate=coding_rate)
    s2 = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s2.setblocking(True)
    i = 0
    while 1 :
        events = lorap2p.events()
        while not (events & LoRa.RX_PACKET_EVENT):
            lorap2p.callback(LoRa.RX_PACKET_EVENT, handler=cb_rx)
            if i > 5:
                time.sleep(uos.urandom(1)[0] / 120)
                s2.send("ping")
                print("retry {}".format(i-5))
                time.sleep(0.5)
            if i>3:    
                pycom.rgbled(0x100000)

            time.sleep(0.5)
            events = lorap2p.events()
            i = i+1
        i=0


mode = 2

if(mode==1) :
    loraWAN()
else:
    loraP2P()
    
