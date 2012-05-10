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
            log.logger.error("[Capteurs] ne peut importer instance.serieCaptInstance")
        self.distance  = 400
        self.listUltrason
        self.listInfrarouge

    def demarrer(self):
        
        if not hasattr(self, 'initialise') or not self.initialise:
            self.initialise = True
            self.serieCaptInstance = __builtin__.instance.serieCaptInstance

    def mesurer(self):
        #retournes l'entier capté
        while len(self.listUltrason) < 3:
            try:
                self.serieCaptInstance.ecrire("ultrason")
                mesure = int(self.serieCaptInstance.lire())
                self.listUltrason.append(int(mesure))
            except:
                pass
            
        while len(self.listInfrarouge) < 3:
            try:
                self.serieCaptInstance.ecrire("ultrason")
                mesure = int(self.serieCaptInstance.lire())
                self.listInfrarouge.append(int(mesure))
            except:
                pass
            
        try:
            self.serieCaptInstance.ecrire(";s")
            mesure = int(self.serieCaptInstance.lire())
            if(string(mesure) == "norespone"):
                mesure = 0
            self.listUltrason.append(int(mesure))
            self.listUltrason.pop(0)
                
        except:
            pass
        
        try:
            self.serieCaptInstance.ecrire(";i")
            mesure = int(self.serieCaptInstance.lire())
            self.listInfrarouge.append(int(mesure))
            self.listInfrarouge.pop(0)
        except:
            pass
        listCopyInfr = self.listInfrarouge
        listCopyUltra = self.listUltrason
        
        self.listInfrarouge.sort()
        self.listUltrason.sort()
        
        if self.listInfrarouge[1] > self.listUltrason[1]:
            return self.listInfrarouge
        else:
            return self.listUltrason
        
        
    def arreter(self):
        """
        Arrêter le capteur (avec liaison série)
        """
        self.initialise = False
        self.stop()
        log.logger.info("[Capteurs] Arrêt du capteur")