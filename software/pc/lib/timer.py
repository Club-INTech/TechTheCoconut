# -*- coding:utf-8 -*-

import time
import threading
import robot

class Timer(threading.Thread):
    """
    Cette classe permet de gérer le timer, afin de minuter la stratégie
    
    :param origine: Origine du temps. (i.e. timestamp à l'allumage)
    :type origine: float (secondes)
    """
    
    def __init__(self):
        Timer.ori  = time.time()
        threading.Thread.__init__(name="timer", target=self.getTime)
        
        
    def getTime(self) :
        return time.time() - Timer.ori
        
    def interrput(self) :
        if self.getTime() >= 90 :
            #TODO UTILISER LA METHODE self.stop() DE LA CLASSE ROBOT
            pass
            
