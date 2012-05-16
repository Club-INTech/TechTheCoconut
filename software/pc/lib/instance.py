# -*- coding: utf-8 -*-

import lib.log
import robot
import asservissement
import asservissementDuree
import recherche_chemin.thetastar
import balise
import capteur
import jumper
import serial
import serie_acquisition
import serie
import script
import attributions
import strategie
import threading
import actionneur
import actionneurSimu
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
        
        #recherche des périphériques
        self.chemins = attributions.attribuer()
        
        # Timeout du script courant, mis à jour par la stratégie
        self.timeout = 1000
        

    def instanciation(self):
        self.instanciationMutex()
        self.instanciationRobot()
        self.instanciationSerie()
        self.instanciationCapteur()
        self.instanciationJumper()
        self.instanciationThetha()
        self.instanciationAsservissement()
        self.instanciationActionneur()
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
                self.serieCaptActionneurInstance = serie.Serie(cheminCapteurs_actionneurs, 9600, 1)
            except :
                log.logger.error("instance : serieCaptActionneurInstance n'est pas chargé. pb d'instanciation de la série.")
        else:
            log.logger.error("instance : serieCaptActionneurInstance n'est pas chargé. pas de chemin trouvé.")
        
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
        
    def ajouterRobotAdverse(self, position, recalculer = True):
        self.liste_robots_adv.append(position)
        if recalculer:
            #retracer le graphe
            self.theta.enregistreGraphe()
    
    def viderListeRobotsAdv(self,recalculer = True):
            self.liste_robots_adv = []
            if recalculer:
                #retracer le graphe
                self.theta.enregistreGraphe()
            
    def instanciationScript(self):
        self.scriptInstance = script.Script()
        
    def instanciationThetha(self):
        log.logger.info("établissement du graphe en fonction des robots adverses rencontrés")
        self.theta = recherche_chemin.thetastar.Thetastar()
        self.theta.enregistreGraphe()
        
    def instanciationStrategie(self):
        try:
            self.strategieInstance = strategie.Strategie()
        except:
            log.logger.error("instance : strategieInstance n'est pas chargé")

    def instanciationCapteur(self):
        self.capteurInstance = capteur.Capteur()
        #except : log.logger.error("instance : capteurInstance n'est pas chargé")

    def instanciationRobot(self):
        self.robotInstance = robot.Robot()

    def instanciationJumper(self) :
        self.jumperInstance = jumper.Jumper()

    def instanciationAsservissement(self):
        try : 
            self.asserInstance = asservissement.Asservissement()
        except :
            log.logger.error("instance : asserInstance n'est pas chargé")
        #try : 
        self.asserInstanceDuree = asservissementDuree.Asservissement_duree()
        #except :
            #log.logger.critical("instance : asserInstanceDuree n'est pas chargé")

    def instanciationActionneur(self):
        try:
            self.actionInstance = actionneur.Actionneur()
        except:
            log.logger.error("instance : actionInstance n'est pas chargé")
        #try:
        self.actionInstanceSimu = actionneurSimu.Actionneur_simu()
        #except:
            #log.logger.error("instance : actionInstanceSimu n'est pas chargé")
        
    def instanciationAcquisition(self):
        try :
            self.acquisitionInstance = serie_acquisition.Serie_acquisition()

        except:
            log.logger.error("instance : acquisitionInstance n'est pas chargé")

    def instanciationMutex(self):
        self.mutex = Lock()
    