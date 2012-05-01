# -*- coding: utf-8 -*-

import lib.log
import robot
import asservissementSimu
import script
import strategie
import threading
import actionneurSimu

from threading import Lock

log =lib.log.Log(__name__)

class Instance:
    """
    Classe pour créer des instances des classes importantes
    :param robotInstance: Instance de la classe robot
    :param asserInstance: Instance de la classe asservissement
    :param actionInstance: Instance de la classe actionneurs
    """
    
    def __init__(self):
        log.logger.info("Instanciation de la classe Instance")
        
        #liste (globale) des centres de robots adverses détectés
        self.liste_robots_adv = []

    def instanciation(self):
        self.instanciationMutex()
        self.instanciationRobot()
        self.instanciationAsservissement()
        self.instanciationActionneur()
        self.instanciationScript()
        self.instanciationStrategie()
        
        
    def ajouterRobotAdverse(self, position):
        self.liste_robots_adv.append(position)
    
    def viderListeRobotsAdv(self):
            self.liste_robots_adv = []
            
    def instanciationScript(self):
        self.scriptInstance = script.Script()
        
    def instanciationStrategie(self):
        try:
            self.strategieInstance = strategie.Strategie()
        except:
            log.logger.error("instance : strategieInstance n'est pas chargé")

    def instanciationRobot(self):
        self.robotInstance = robot.Robot()
        
    def instanciationAsservissement(self):
        try : 
            self.asserInstance = asservissementSimu.Asservissement()
        except :
            log.logger.error("instance : asserInstance n'est pas chargé")

    def instanciationActionneur(self):
        try: self.actionInstance = actionneurSimu.Actionneur()
        except: log.logger.error("instance : actionInstance n'est pas chargé")
        
    def instanciationMutex(self):
        self.mutex = Lock()
    