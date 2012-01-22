# -*- coding: utf-8 -*-

import serial

import log
log = log.Log()

class Serie(serial.Serial):
    """
    Classe de créer une liaison Série
    
    :param peripherique: chemin du périphérique utilisant la liaison série
    :type peripherique: string
    :param debit: Débit de baud de la liaison
    :type debit: int
    :param timeout: Timeout de la liaison en secondes
    :type timeout: int
    :TODO: Utiliser un thread
    :TODO: Mettre le débit de Baud par défaut
    """
    def __init__(self, peripherique, debit, timeout):
        self.peripherique = peripherique
        log.logger.info("Initialisation de la liaison série sur "+peripherique+" avec un débit de baud de "+str(debit)+" et un timeout de "+str(timeout))
        try:
            serial.Serial.__init__(self, peripherique, debit, timeout=timeout)
        except:
            log.logger.error("Erreur d'initialisation de la liaison série sur "+peripherique+" avec un débit de baud de "+str(debit)+" et un timeout de "+str(timeout))

    def ecrire(self, msg):
        """
        Écrire une information vers un périphérique puis retourner à la ligne
        
        :param msg: message à donner au périphérique
        :type msg: string
        """
        log.logger.debug("Écrire sur la liaison série "+self.peripherique+" : "+msg)
        self.write(msg+"\r\n")
    
    def lire(self):
        """
        Lire une information venant d'un périphérique jusqu'au retour à la ligne
        
        :return: Chaîne lue
        :rtype: string
        :TODO: Finir cette fonction
        """
        lu = ""
        log.logger.debug("Lecture sur la liaison série "+self.peripherique+" : "+lu)
        return lu;

    def __del__(self):
        """
        Destructeur qui ferme proprement la liaison série
        """
        log.logger.info("Suppression de la liaison série sur "+self.peripherique)
        self.close()