# -*- coding: utf-8 -*-


import log
import __builtin__

log = log.Log(__name__)


class Capteur():
    """
    Classe permettant de gérer un capteur
    
    :param nom: Nom à donner au thread
    :type nom: string
    :param nombreEchantillons: Nombre de prises à faire pour éviter les erreurs de mesure
    :type nombreEchantillons: int
    :param distance: Distance capté en mm à partir de laquelle on prévoit un évitemment
    :type distance: long
    """
    def __init__(self):
        if hasattr(__builtin__.instance, 'serieCaptInstance'):  
            self.demarrer()
        else:
            log.logger.error("l'instance de lib.capteur.Capteur n'est pas chargée")
        self.distance  = 400

    def demarrer(self):
        
        if not hasattr(self, 'initialise') or not self.initialise:
            self.initialise = True
            self.serieInstance = __builtin__.instance.serieCaptInstance

    def mesurer(self):
        #retourne l'entier capté
        self.serieInstance.ecrire("ultrason\n\r")
        mesure = int(str(self.serieInstance.lire()))
        return mesure
        
    def arreter(self):
        """
        Arrêter le capteur (avec liaison série)
        """
        self.initialise = False
        self.stop()
        log.logger.info("Arrêt du capteur")