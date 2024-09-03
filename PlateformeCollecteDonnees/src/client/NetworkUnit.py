from queue import Queue
import sys

data_format = { 'eui' : None, 'timestamp':"", 'luminosity':None, 'pression':None, 'temperature':None,
                'longitude':None, 'latitude':None, 'altitude':None, 'angle':None, 
                'vitesse_angulaire_X':None, 'vitesse_angulaire_Y':None, 'vitesse_angulaire_Z':None,
                'acceleration_X':None, 'acceleration_Y':None, 'acceleration_Z':None,
                'azimuth':None, 'distance_recul':None, 'presence':None , 'humidite':None,  'distance_recul':None}
LTE_connection = 0

def SendLoRa(message):
    #TODO:
    # Send through STM (UART/USB)

    pass

def SendLTE(message):
    #TODO:
    # Send through ESP (UART/USB)


    pass


def Sendnode(Q_input : Queue, network_state : Queue, Config):
    global LTE_connection
    try:
        while True:
            # If we have LTE connection we use it, else we use LoRa.
            if not network_state.empty():
                LTE_connection = network_state.get()
            
            if not Q_input.empty():
                
                if LTE_connection>0 :
                    SendLTE(Q_input.get())
                else:
                    while not Q_input.empty():
                        message = Q_input.get()
                    SendLoRa(message)

    except KeyboardInterrupt :
        sys.exit(0)