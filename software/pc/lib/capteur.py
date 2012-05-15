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
        
        self.demarrer()
        self.distance  = 400
        self.listUltrason = []
        self.listInfrarouge = []

    def demarrer(self):
        if not hasattr(Capteur, 'initialise') or not Capteur.initialise:
            Capteur.initialise = True
            if hasattr(__builtin__.instance, 'serieCaptActionneurInstance'):
                self.serieCaptActionneurInstance = __builtin__.instance.serieCaptActionneurInstance
            else:
                log.logger.error("[Capteurs] impossible d'acceder à serieCaptActionneurInstance")

    def mesurer(self):
        #retournes l'entier capté
        while len(self.listUltrason) < 5:
            try:
                self.serieCaptActionneurInstance.ecrire(";s")
                mesure = int(self.serieCaptActionneurInstance.lire())
                self.listUltrason.append(int(mesure))
            except:
                pass
            
        while len(self.listInfrarouge) < 5:
            try:
                self.serieCaptActionneurInstance.ecrire(";i")
                mesure = int(self.serieCaptActionneurInstance.lire())
                self.listInfrarouge.append(int(mesure))
            except:
                pass
            
        try:
            self.serieCaptActionneurInstance.ecrire(";s")
            mesure = int(self.serieCaptActionneurInstance.lire())
            try:
                if(string(mesure) == "norespone") or mesure < 0:
                    mesure = 0
            except:
                pass
            print "ultrason : >"+str(mesure)+"<"
            self.listUltrason.append(int(mesure))
            self.listUltrason.pop(0)
                
        except:
            pass
        
        try:
            self.serieCaptActionneurInstance.ecrire(";i")
            mesure = int(self.serieCaptActionneurInstance.lire())
            if mesure > 1500 or mesure < 0:
                mesure = 0
            print "infrarouge : >"+str(mesure)+"<"
            self.listInfrarouge.append(mesure)
            self.listInfrarouge.pop(0)
        except:
            pass
        
        listCopyInfr = self.listInfrarouge[:]
        listCopyUltra = self.listUltrason[:]
        
        listCopyInfr.sort()
        listCopyUltra.sort()
        
        print "résultat : "+str(max(listCopyInfr[3],listCopyUltra[3]))+"\n"
        return max(listCopyInfr[3],listCopyUltra[3])
        
        
    def arreter(self):
        """
        Arrêter le capteur (avec liaison série)
        """
        self.initialise = False
        self.stop()
        log.logger.info("[Capteurs] Arrêt du capteur")