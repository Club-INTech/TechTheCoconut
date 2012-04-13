# -*- coding:utf-8 -*-

import time
import threading
import robot
import strategie
import sys
import signal
import os

import log
log = log.Log(__name__)

import __builtin__

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
        
        # Création du thread d'arrêt du robot
        threading.Thread.__init__(self, target=self.interrupt, name="arretRobot")
        
    def lancer(self) :
        """
        Permet de lancer une bonne fois pour toute le timer
        """
        
        log.logger.info("Lancement du timer...")
        
        # Origine des temps pour self.getTime()
        Timer.origine = time.time()
        
        # Lancement du thread d'arrêt du robot
        self.start()
        
        
    def getTime(self) :
        """
        Retourne le nombre de secondes écoulées depuis :
            - L'appel de self.lancer()
            - Le lancement de iPython si la dernière méthode n'a jamais été lancée
        """
        
        return time.time() - Timer.origine
        
    def interrupt(self) :
        
        # Durée du math
        tempsFinal = constantes["DureeJeu"]
        
        time.sleep(tempsFinal)
        
        # Suicide :D
        os.kill(os.getpid(), signal.SIGUSR1)
        
        ## Arrêt de la prise de stratégie
        #strategie.Strategie().arreterPrendreDecisions()
        
        ## Arrêt de l'asservissement.
        #try : 
            #__builtin__.instance.asserInstance.setUnsetAsser("translation", 0)
            #__builtin__.instance.asserInstance.setUnsetAsser("rotation", 0)
        #except : log.logger.error("Impossible d'arreter l'asservissement")
        
        ## Arrêt des actionneurs
        #try :
            #__builtin__.instance.actionInstance.stop()
        #except :
            #log.logger.error("Impossible d'arrêter les actionneurs")
        
        ## Arrêt des capteurs
        #try :
            #__builtin__.instance.serieCaptInstance.close()
        #except :
            #log.logger.error("Impossible d'arrêter les capteurs")
        
        
        log.logger.info("Arrêt du robot après " + str(tempsFinal) + " secondes")
