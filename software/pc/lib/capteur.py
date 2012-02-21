# -*- coding: utf-8 -*-

import serie
import log
import peripherique

log = log.Log()


class Capteur:
    """
    Classe permettant de gérer un capteur
    
    :param peripherique: chemin du périphérique utilisant la liaison série
    :type peripherique: string
    :param nom: Nom à donner au thread
    :type nom: string
    :param debit: Débit de baud de la liaison
    :type debit: int
    :param timeout: Timeout de la liaison en secondes
    :type timeout: int
    :param parite: Type de parité
    :type parite: None|'PARITY_NONE'|'PARITY_EVEN'|'PARITY_ODD'|'PARITY_MARK'|'PARITY_SPACE'
    
    
    """
    def __init__(self, peripherique, nom, debit, timeout, parite=None, nombreEchantillons=3):
        self.peripherique = peripherique
        self.nom = nom
        self.debit = debit
        self.timeout = timeout
        self.parite = parite
        self.serie = serie.Serie(peripherique, nom, debit, timeout, parite)
        self.nombreEchantillons = nombreEchantillons
    
    
    def lire(self):
        """
        Cette méthode permet de lire les informations d'un capteur
        
        :return: [val_capteur_1, val_capteur_2, val_capteur_3]
        :rtype: tableau de float (?)
        
        """
        # Ouverture de la liaison série
        self.serie.start()
        
        """
        Architecture d'un message sur la liaison série :
        |   'd'
        |   valeur_capteur_1
        |   valeur_capteur_2
        |   valeur_capteur_3
        |   'f'
        """
        
        compteur = 0
        val = [0,0,0]
        
        while compteur < self.nombreEchantillons :
            if self.serie.lire() != 'd' :
                log.logger.error("Erreur : le message du capteur "+self.peripherique+" ne commence pas par le caractère 'd'")
                self.serie.stop()
                compteur = nombreEchantillons
                #TODO Faut-il stopper l'exécution de la fonction ?
                
             val[0] = (compteur/nombreEchantillons)*val[0] + int(self.serie.lire())/nombreEchantillons
             val[1] = (compteur/nombreEchantillons)*val[1] + int(self.serie.lire())/nombreEchantillons
             val[2] = (compteur/nombreEchantillons)*val[2] + int(self.serie.lire())/nombreEchantillons

            if self.serie.lire() != 'f' :
                log.logger.error("Erreur : le message du capteur "+self.peripherique+" ne finit pas par le caractère 'f'")
                self.serie.stop()
                compteur = nombreEchantillons
                
        
        self.serie.stop()
        
        return val
        
             
      