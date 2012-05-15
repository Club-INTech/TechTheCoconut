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
        if hasattr(__builtin__.instance, 'serieCaptActionneurInstance'):  
            self.demarrer()
        else:
            log.logger.error("l'instance de lib.capteur.Capteur n'est pas chargée")
        
    def demarrer(self):
        if not hasattr(self, 'initialise') or not self.initialise:
            self.initialise = True
            self.serieCaptActionneurInstance = __builtin__.instance.serieCaptActionneurInstance
            
    def getEtat(self) :
        """
        Retourne l'état du Jumper (1 si enfoncé, 0 sinon)
        """
        while 1:
            self.serieCaptActionneurInstance.ecrire(";j")
            try :
                return int(self.serieCaptActionneurInstance.lire())
            except :
                time.sleep(0.01)
        
    def demarrerRecalage(self) :
        """
        Se met en attente d'un 1
        """
        lancer = True
        while lancer :
            lancer = self.getEtat()
        
        
        
    def scruterDepart(self):
        """
        Se met en attente d'un 0
        """
        attente = False
        while not attente :
            attente = self.getEtat()
        
        
            
            
            