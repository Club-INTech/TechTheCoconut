# -*- coding:utf-8 -*-

import time
import threading
import robot

import log
log = log.Log(__name__)

class Timer(threading.Thread):
    """
    Cette classe permet de gérer le timer, afin de minuter la stratégie
    et d'arrêter le robot après 90sec
    
    :param origine: Origine du temps. (i.e. timestamp à l'allumage)
    :type origine: float (secondes)
    """
    
    def __init__(self):
        Timer.origine  = constantes["t0"]  # Cette variable est crée par le lanceur
                                           # TODO utiliser la variable crée par le bumper de démarrage
                                           # 
                                           
        threading.Thread.__init__(self, target=self.interrupt, name="Timer")
        
    def lancer(self) :
        """
        Permet de lancer une bonne fois pour toute le timer
        """
        
        log.logger.info("Lancement du timer...")
        Timer.origine = time.time()
        
        self.start()
        
        
    def getTime(self) :
        return time.time() - Timer.origine
        
    def interrupt(self) :
        tempsFinal = 10
        time.sleep(tempsFinal)
        #TODO UTILISER LA METHODE self.stop() DE LA CLASSE ROBOT
        #TODO Pour l'intant, cette fonction ne fait rien.
        log.logger.info("Arrêt du robot après " + str(tempsFinal) + " secondes")
