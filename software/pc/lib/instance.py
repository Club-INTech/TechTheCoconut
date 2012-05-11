# -*- coding: utf-8 -*-

import lib.log
import robot
import asservissement
import asservissementDuree
import balise
import capteur
import serial
import serie_acquisition
import serie
import script
import attributions
import strategie
import threading
import actionneur
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
        self.instanciationMutex()
        self.instanciationRobot()
        self.instanciationSerie()
        self.instanciationCapteur()
        self.instanciationAsservissement()
        self.instanciationActionneur()
        #self.instanciationAcquisition()
        self.instanciationScript()
        self.instanciationStrategie()
        self.baliseInstance = balise.Balise()
        
    
    def instanciationSerie(self):
        
        #Instance serie asservissement
        cheminAsser = self.chemins[0]
        if cheminAsser:
            try:
                self.serieAsserInstance = serie.Serie(cheminAsser, 9600, 3)
            except :
                log.logger.error("instance : serieAsserInstance n'est pas chargé. pb d'instanciation de la série.")
        else:
            log.logger.error("instance : serieAsserInstance n'est pas chargé. pas de chemin trouvé.")
            
        #Instance serie Balise
        cheminBalise = self.chemins[2]
        if cheminBalise:
            try:
                self.serieBaliseInstance = serie.Serie(cheminBalise, 9600, 1)
            except :
                log.logger.error("instance : serieBaliseInstance n'est pas chargé. pb d'instanciation de la série.")
        else:
            log.logger.error("instance : serieBaliseInstance n'est pas chargé. pas de chemin trouvé.")
            
        #Instance serie Capteur-Actionneurs (une seule carte)
        cheminCapteurs_actionneurs = self.chemins[3]
        if cheminCapteurs_actionneurs:
            try:
                self.serieCaptInstance = serie.Serie(cheminCapteurs_actionneurs, 9600, 1)
                self.serieActionneurInstance = self.serieCaptInstance
            except :
                log.logger.error("instance : serieCaptInstance et serieActionneurInstance ne sont pas chargés. pb d'instanciation de la série.")
        else:
            log.logger.error("instance : serieCaptInstance et serieActionneurInstance ne sont pas chargés. pas de chemin trouvé.")
        
        """
        #Instance serie Capteurs indépendants (sur Arduino)
        cheminCapt = self.chemins[1]
        if cheminCapt:
            try:
                self.serieCaptInstance = serie.Serie(cheminCapt, 57600, 1)
            except :
                log.logger.error("instance : serieCaptInstance n'est pas chargé. pb d'instanciation de la série.")
        else:
            log.logger.error("instance : serieCaptInstance n'est pas chargé. pas de chemin trouvé.")
            
        #Instance serie Actionneurs indépendants (sur Arduino)
        cheminActionneur = self.chemins[4]
        if cheminActionneur :
            try:
                self.serieActionneurInstance = serie.Serie(cheminActionneur, 9600, 1)
            except :
                log.logger.error("instance : serieActionneurInstance n'est pas chargé. pb d'instanciation de la série.")
        else :
            log.logger.error("instance : serieActionneurInstance n'est pas chargé. pas de chemin trouvé.")
        """
        
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

    def instanciationCapteur(self):
        try : self.capteurInstance = capteur.Capteur()
        except : log.logger.error("instance : capteurInstance n'est pas chargé")

    def instanciationRobot(self):
        self.robotInstance = robot.Robot()
        
    def instanciationAsservissement(self):
        try : 
            self.asserInstance = asservissement.Asservissement()
        except :
            log.logger.error("instance : asserInstance n'est pas chargé")
        try : 
            self.asserInstanceDuree = asservissementDuree.Asservissement_duree()
        except :
            log.logger.critical("instance : asserInstanceDuree n'est pas chargé")

    def instanciationActionneur(self):
        try: self.actionInstance = actionneur.Actionneur()
        except: log.logger.error("instance : actionInstance n'est pas chargé")
        
    def instanciationAcquisition(self):
        try :
            self.acquisitionInstance = serie_acquisition.Serie_acquisition()

        except:
            log.logger.error("instance : acquisitionInstance n'est pas chargé")

    def instanciationMutex(self):
        self.mutex = Lock()
    