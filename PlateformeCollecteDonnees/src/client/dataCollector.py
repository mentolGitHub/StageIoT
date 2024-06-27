from queue import Queue
import sys


def save_DB(item):
    #TODO:
    pass



def dataCollectornode(listeQ_input : Queue[10], Q_output : Queue, Q_send_serv : Queue):
    # setup DB locale
    

    try:
        while True:
            #TODO:

            data = {}




            save_DB(data)
            Q_send_serv.put(data)
            Q_output.put(data)

            pass
    except KeyboardInterrupt :
        sys.exit(0)
    