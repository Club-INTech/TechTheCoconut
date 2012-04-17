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
<<<<<<< HEAD
        self.serieInstance.ecrire("ultrason\n\r")
        mesure = int(str(self.serieInstance.lire()).replace("\n","").replace("\r","").replace("\0",""))
        return mesure
=======
        try :
            self.serieInstance.write("ultrason\r")
            mesure = int(str(self.serieInstance.readline()).replace("\n","").replace("\r","").replace("\0",""))
            return mesure
        except :
            return self.mesurer()
>>>>>>> 46fb56d2be6a0bbe391376d3048c22501c061b60
        
    def arreter(self):
        """
        Arrêter le capteur (avec liaison série)
        """
        self.initialise = False
        self.stop()
        log.logger.info("Arrêt du capteur")