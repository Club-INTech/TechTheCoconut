# -*- coding: utf-8 -*-

import serial

import log
log = log.Log(__name__)

class SerieSimple(serial.Serial):
    """
    Classe de créer une liaison Série sans Thread (ie bloquante)
    
    :param peripherique: chemin du périphérique utilisant la liaison série
    :type peripherique: string
    :param debit: Débit de baud de la liaison
    :type debit: int
    :param timeout: Timeout de la liaison en secondes
    :type timeout: int
    :TODO: Mettre le débit de Baud par défaut
    """
    def __init__(self, peripherique, debit, timeout):
        self.peripherique = peripherique
        log.logger.info("Initialisation de la liaison série simple sur "+peripherique+" avec un débit de baud de "+str(debit)+" et un timeout de "+str(timeout))
        try:
            serial.Serial.__init__(self, peripherique, debit, timeout=timeout)
        except:
            log.logger.error("Erreur d'initialisation de la liaison série simple sur "+peripherique+" avec un débit de baud de "+str(debit)+" et un timeout de "+str(timeout))

    def ecrire(self, msg):
        """
        Écrire une information vers un périphérique puis retourner à la ligne
        
        :param msg: message à donner au périphérique
        :type msg: string
        :return: Nombre de caractères envoyés
        :rtype: int
        """
        
        log.logger.debug("Écrire sur la liaison série  " + str(self.peripherique) + " : " + str(msg))
        return self.write(msg+"\r\n")
    
    def lire(self):
        """
        Lire une information venant d'un périphérique jusqu'au retour à la ligne
        
        :return: Chaîne lue
        :rtype: string
        """
        lu = self.readline()
        lu = lu.split("\r\n")[0]
        log.logger.debug("Lecture sur la liaison série "+self.peripherique+" : "+lu)
        return lu;

    def stop(self):
        """
        Destructeur qui ferme proprement la liaison série
        """
        log.logger.info("Suppression de la liaison série sur "+self.peripherique)
        self.close()