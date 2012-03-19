# -*- coding: utf-8 -*-

import sys
import os
import lib.log
import robot
import peripherique
import asservissement
import serial


log =lib.log.Log(__name__)

class Instance:
    """
    Classe pour créer des instances des classes importantes
    :param robotInstance: Instance de la classe robot
    :param capteurInstance: Instance de la classe capteur
    :param asserInstance: Instance de la classe asservissement
    :param serieAsserInstance: Instance de la classe serie pour l'asservissement
    :param serieCaptInstance: Instance de la classe  serie pour les capteurs/actionneurs
    """
    
    def __init__(self):
        log.logger.info("Instanciation de la classe Instance")

    def instanciation(self):
        self.instanciationRobot()
        self.instanciationSerie()
        self.instanciationAsservissement()
        self.instanciationCapteur()
    
    def instanciationCapteur(self):
        self.capteurInstance = lib.capteur.Capteur()

    def instanciationRobot(self):
        self.robotInstance = robot.Robot()
        
    def instanciationAsservissement(self):
        self.asserInstance = asservissement.Asservissement()

    def instanciationSerie(self):
        #Instance serie asservissement
        cheminAsser = lib.peripherique.chemin_de_peripherique("asservissement")
        if cheminAsser:
            self.serieAsserInstance = serial.Serial(cheminAsser, 9600, timeout=0)
        else:
            log.logger.error("L'asservissement n'est pas chargé")
            
            
        cheminCapt = peripherique.chemin_de_peripherique("capteur")
        if cheminCapt:
            self.serieCaptInstance = serial.Serial(cheminCapt, 57600, timeout=3)
        else:
            log.logger.error("Le capteur "+self.nom+" n'est pas chargé")
        
        

        