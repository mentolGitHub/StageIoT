from queue import Queue
import sys


LTE_connection = 0

def SendLoRa(message):
    #TODO:
    pass

def SendLTE(message):
    #TODO:
    pass


def Sendnode(Q_input : Queue, network_state : Queue):
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
                    message
                    while not Q_input.empty():
                        message = Q_input.get()
                    SendLoRa(message)

    except KeyboardInterrupt :
        sys.exit(0)