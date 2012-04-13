# -*- coding:utf-8 -*-

import log
import time
import __builtin__

log = log.Log(__name__)


class Jumper :
    """
    classe gérant le Jumper
    """
    
    def __init__(self) :
        self.endmsg = "\n\r"
        
        if hasattr(__builtin__.instance, 'serieCaptInstance'):  
            self.demarrer()
        else:
            log.logger.error("l'instance de lib.capteur.Capteur n'est pas chargée")
        
    def demarrer(self):
        if not hasattr(self, 'initialise') or not self.initialise:
            self.initialise = True
            self.serieInstance = __builtin__.instance.serieCaptInstance
            
    def getEtat(self) :
        """
        Retourne l'état du Jumper (1 si enfoncé, 0 sinon)
        """
        while 1:
            self.serieInstance.write("jumper\n\r")
            try :
                return int(self.serieInstance.readline().replace("\n", "").replace("\r", "").replace("\0", "").replace("\n", ""))
            except :
                time.sleep(0.01)
        
    def demarrerRecalage(self) :
        """
        Se met en attente d'un 1
        """
        lancer = False
        while not lancer :
            lancer = self.getEtat()
        
        
        
    def scruterDepart(self):
        """
        Se met en attente d'un 0
        """
        attente = True
        while attente :
            attente = self.getEtat()
        
        
            
            
            