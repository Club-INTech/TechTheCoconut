# -*- coding: utf-8 -*-

import __builtin__
import threading
from threading import Lock

class Serie_acquisition:
    
    def __init__(self):
        if hasattr(__builtin__.instance, 'robotInstance'):
            self.robotInstance = __builtin__.instance.robotInstance
        else:
            log.logger.error("l'instance de instance.robotInstance n'est pas chargée")
            
        if hasattr(__builtin__.instance, 'serieAsserInstance'):
            self.serieAsserInstance = __builtin__.instance.serieAsserInstance
        else:
            log.logger.error("l'instance de instance.serieAsserInstance n'est pas chargée")
            
        if hasattr(__builtin__.instance, 'mutex'):
            self.mutex = __builtin__.instance.mutex
        else:
            log.logger.error("L'instance du mutex n'est pas chargée")
        
        
        self.robotPosition = math.point.Point(0,0)
        self.asserInstance = __builtin__.instance.asserInstance
        #thread = threading.Thread(target = self.ecoute_thread)
        #thread.start()
    
    def ecoute_thread(self):
        while 42:
            self.mutex.acquire()
            self.serieAsserInstance.write("pos\n")
            reponse = self.serieAsserInstance.readline()
            reponse = str(reponse).replace("\n","").replace("\r","").replace("\0", "")
            #self.robotPosition = 
            self.robotInstance.
            self.mutex.release()