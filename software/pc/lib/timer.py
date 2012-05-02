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
        Timer.origine  = time.time() 
        Timer.origineStrategie = time.time()
        
        # Création du thread d'arrêt du robot
        threading.Thread.__init__(self, target=self.interrupt, name="arretRobot")
        
    def lancer(self) :
        """
        Permet de lancer une bonne fois pour toute le timer
        """
        
        log.logger.info("Lancement du timer...")
        
        # Origine des temps pour self.getTime()
        Timer.origineStrategie = time.time()
        
        # Lancement du thread d'arrêt du robot
        self.start()
        
        
    def getTime(self, strategie=True) :
        """
        Retourne le nombre de secondes écoulées depuis :
            - L'appel de self.lancer()
            - Le lancement de iPython si la dernière méthode n'a jamais été lancée
            
        :param strategie: A mettre à 1 si on veut retourner le temps utilisé depuis le lancement de la strat.
        :type strategie: Bool
        
        """
        if strategie:
            return time.time() - Timer.origineStrategie
        else :
            return time.time() - Timer.origine
        
    def interrupt(self) :
        
        # Durée du math
        try:
            tempsFinal = constantes["DureeJeu"]
        except:
            tempsFinal = 87;
        
        time.sleep(tempsFinal)
        
        ## Arrêt de l'asservissement.
        try:
            __builtin__.instance.asserInstance.immobiliser()
            time.sleep(1)
            __builtin__.instance.asserInstance.setUnsetAsser("translation", 0)
            __builtin__.instance.asserInstance.setUnsetAsser("rotation", 0)
        except: log.logger.error("Impossible d'arreter l'asservissement")
        
        ## Arrêt des actionneurs
        try:
            __builtin__.instance.actionInstance.stop()
        except:
            log.logger.error("Impossible d'arrêter les actionneurs")
        
        ## Arrêt des capteurs
        try:
            __builtin__.instance.serieCaptInstance.close()
        except:
            log.logger.error("Impossible d'arrêter les capteurs")
        
        try:
            log.logger.info("Arrêt du robot après " + str(tempsFinal) + " secondes")
        except:
            pass

        # Suicide :D
        os.kill(os.getpid(), signal.SIGUSR1)