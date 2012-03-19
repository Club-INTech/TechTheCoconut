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
    """
    
    def __init__(self):
        log.logger.info("Instanciation de la classe Instance")

    def instanciationRobot(self):
        self.robotInstance = robot.Robot()

    def instanciationSerie(self):
        #Instance serie asservissement
        chemin = lib.peripherique.chemin_de_peripherique("asservissement")
        if chemin:
            self.serieAsserInstance = serial.Serial(chemin, 9600, timeout=0)
        else:
            log.logger.error("L'asservissement n'est pas chargé")
        
    def instanciationAsservissement(self):
        self.asserInstance = asservissement.Asservissement()
        

        