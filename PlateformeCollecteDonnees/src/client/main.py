from queue import Queue
import sys
import threading
import time

import dataCollector
import NetworkUnit
import MiddlewareUnit


def init_client():
    #TODO:
    pass


def run_client():

    listeQ_capteur = [Queue(),Queue()]#...
    Q_send = Queue()
    Q_output = Queue()

    threadMiddleware = threading.Thread(target=MiddlewareUnit.Middlewarenode,args=[listeQ_capteur])
    threadDataCollecter = threading.Thread(target=dataCollector.dataCollectornode,args=[listeQ_capteur,Q_output,Q_send])
    threadSend = threading.Thread(target=NetworkUnit.Sendnode,args=[Q_send,])

    try:
        threadMiddleware.start()
        threadDataCollecter.start()
        threadSend.start()

        while threading.active_count()>1:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        
        sys.exit()
    


def main():

    """
    This is the main function of the Data Collecting plateform client.
    This program uses a MySQL database.
    You can modify some configuration settings in the config.conf file that is in the same folder/directory as this program.
    """

    init_client()
    run_client()


if __name__ == "__main__":
    main()

