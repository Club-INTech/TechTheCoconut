# -*- coding: utf-8 -*-

import serie
import log
import peripherique
import __builtin__

log = log.Log(__name__)


class Capteur(serie.Serie):
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

    def demarrer(self):
        
        if not hasattr(Capteur, 'initialise') or not Capteur.initialise:
            Capteur.initialise = True
            self.serieInstance = __builtin__.instance.serieCaptInstance

    def mesurer(self):
        """
        Cette méthode permet de lire les informations d'un capteur
        
        :return: [val_capteur_1, val_capteur_2, val_capteur_3]
        :rtype: tableau de float
        
        """
        
        """
        Architecture d'un message sur la liaison série :
        |   'd'
        |   valeur_capteur_1
        |   valeur_capteur_2
        |   valeur_capteur_3
        |   'f'
        """
        mesure = self.file_attente.get(True, 3)
            
        """ A modifier (peut-être) quand il y aura les trois capteurs.
        compteur = 0
        val = [0,0,0]
        while compteur < self.nombreEchantillons:
            # On commence quand on reçoit 'd'
            while not self.file_attente.empty() and self.file_attente.get() == 'd':
                # On rejette la séquence de mesure si une mesure est erronnée
                try:
                    val[0] = (compteur/nombreEchantillons)*val[0] + float(self.file_attente.get(True, 3))/nombreEchantillons
                except:
                    log.logger.error("La première mesure reçue par le capteur "+self.nom+" n'est pas correcte")
                    break
                try:
                    val[1] = (compteur/nombreEchantillons)*val[1] + float(self.file_attente.get(True, 3))/nombreEchantillons
                except:
                    log.logger.error("La deuxième mesure reçue par le capteur "+self.nom+" n'est pas correcte")
                    break
                try:
                    val[2] = (compteur/nombreEchantillons)*val[2] + float(self.file_attente.get(True, 3))/nombreEchantillons
                except:
                    log.logger.error("La troisième mesure reçue par le capteur "+self.nom+" n'est pas correcte")
                    break
                if self.file_attente.get(True, 3) != 'f' :
                    log.logger.error("Le caractère de fin reçu par le capteur "+self.nom+" n'est pas correct")
                    break
                return val
        """
        return mesure
        
    def arreter(self):
        """
        Arrêter le capteur (avec liaison série)
        """
        Capteur.initialise = False
        self.stop()