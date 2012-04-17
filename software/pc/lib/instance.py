# -*- coding: utf-8 -*-

import lib.log
import robot
import asservissement
import capteur
import serial
import serie_acquisition
import script
import attributions
import strategie
import peripherique
import threading
from threading import Lock

log =lib.log.Log(__name__)

class Instance:
    """
    Classe pour créer des instances des classes importantes
    :param robotInstance: Instance de la classe robot
    :param capteurInstance: Instance de la classe capteur
    :param asserInstance: Instance de la classe asservissement
    :param serieAsserInstance: Instance de la classe serie pour l'asservissement
    :param serieCaptInstance: Instance de la classe  serie pour les capteurs/actionneurs
    :param actionInstance: Instance de la classe actionneurs
    """
    
    def __init__(self):
        log.logger.info("Instanciation de la classe Instance")
        
        #liste (globale) des centres de robots adverses détectés
        self.liste_robots_adv = []
        self.chemins = attributions.attribuer()

    def instanciation(self):
        self.instanciationRobot()
        self.instanciationSerie()
        self.instanciationCapteur()
        self.instanciationAsservissement()
        self.instanciationActionneur()
        self.instanciationAcquisition()
        self.instanciationScript()
        self.instanciationStrategie()
        
        
    def ajouterRobotAdverse(self, position):
        self.liste_robots_adv.append(position)
    
    def viderRobotAdverse(self):
            self.liste_robots_adv = []
            
    def instanciationScript(self):
        self.scriptInstance = script.Script()
        
    def instanciationStrategie(self):
        self.strategieInstance = strategie.Strategie()

    def instanciationCapteur(self):
        try : self.capteurInstance = capteur.Capteur()
        except : log.logger.error("Impossible d'instancier capteur")

    def instanciationRobot(self):
        self.robotInstance = robot.Robot()
        
    def instanciationAsservissement(self):
        try : self.asserInstance = asservissement.Asservissement()
        except : log.logger.error("Impossible d'instancier asservissement")

    def instanciationActionneur(self):
        try: self.actionInstance = actionneur.Actionneur()
        except: log.logger.error("Impossible d'instancier actionneur")
        
    def instanciationSerie(self):
        #Instance serie asservissement
        #cheminAsser = lib.peripherique.chemin_de_peripherique("asservissement")
        #cheminAsser = '/dev/ttyUSB9'
        cheminAsser = self.chemins[0]
        if cheminAsser:
            self.serieAsserInstance = serial.Serial(cheminAsser, 9600, timeout=3)
        else:
            log.logger.error("L'asservissement n'est pas chargé")
            
        # Actionneurs ≠ Capteurs sur Arduino pour la Belgique.
        #cheminActionneur = lib.peripherique.chemin_de_peripherique("actionneur")
        
        cheminActionneur = self.chemins[4]
        
        
        if cheminActionneur :
            self.serieActionneurInstance = serial.Serial(cheminActionneur, 9600, timeout = 1)
        else :
            log.logger.error("Les actionneurs ne sont pas chargés")
        
        cheminCapt = peripherique.chemin_de_peripherique("capteur_actionneur")
        #cheminCapt = '/dev/ttyUSB0'
        cheminCapt = self.chemins[1]
        
        if cheminCapt:
            try:
                self.serieCaptInstance = serial.Serial(cheminCapt, 57600, timeout=1)
            except :
                pass
        else:
            log.logger.error("Le capteur n'est pas chargé")
        
    def instanciationAcquisition(self):
        try :
            self.acquisitionInstance = serie_acquisition.Serie_acquisition()

        except:
            log.logger.error("L'acquisition n'est pas chargé")

    def instanciationMutex(self):
        self.mutex = Lock()